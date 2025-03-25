import atexit
import asyncio
import os
import platform
import re
import tarfile
import tempfile
from pathlib import Path
from random import randint

import aiohttp
import subprocess
from tqdm.auto import tqdm

PLATFORM_MAP = {
  ("Windows", "AMD64"): "cloudflared-windows-amd64.exe",
  ("Windows", "x86"): "cloudflared-windows-386.exe",
  ("Linux", "x86_64"): "cloudflared-linux-amd64",
  ("Linux", "i386"): "cloudflared-linux-386",
  ("Linux", "arm"): "cloudflared-linux-arm",
  ("Linux", "arm64"): "cloudflared-linux-arm64",
  ("Linux", "aarch64"): "cloudflared-linux-arm64",
  ("Darwin", "x86_64"): "cloudflared-darwin-amd64.tgz",
  ("Darwin", "arm64"): "cloudflared-darwin-amd64.tgz",
}

DOWNLOAD_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/"

def get_executable_name():
  """Gets the Cloudflare binary name for the current system."""
  system, arch = platform.system(), platform.machine()
  binary_name = PLATFORM_MAP.get((system, arch))
  if not binary_name:
    raise RuntimeError(f"Unsupported platform: {system} {arch}")
  return binary_name

async def download_file(url, destination):
  """Downloads a file asynchronously with a progress bar."""
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      response.raise_for_status()
      file_size = int(response.headers.get("content-length", 50_000_000))

      with open(destination, "wb") as file, tqdm(
        desc=" * Fetching Cloudflared",
        total=file_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
      ) as progress:
        async for chunk in response.content.iter_chunked(8192):
          file.write(chunk)
          progress.update(len(chunk))

def extract_tar(archive_path, destination):
  """Extracts a tar file."""
  with tarfile.open(archive_path, "r") as tar:
    tar.extractall(destination)

async def ensure_binary():
  """Ensures the Cloudflare binary is downloaded and updated."""
  system, arch = platform.system(), platform.machine()
  binary_name = get_executable_name()
  temp_dir = Path(tempfile.gettempdir())
  binary_path = temp_dir / ("cloudflared" if system == "Darwin" else binary_name)

  if binary_path.exists():
    try:
      subprocess.Popen([str(binary_path), "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
      print(f" * Warning: Could not update Cloudflared - {e}")
    return str(binary_path)

  print(f" * Downloading Cloudflare tunnel for {system} {arch}...")
  download_path = temp_dir / binary_name
  await download_file(DOWNLOAD_URL + binary_name, str(download_path))

  if system == "Darwin":
    extract_tar(str(download_path), str(temp_dir))

  os.chmod(str(download_path), 0o777)
  return str(download_path)

async def start_tunnel(app_port=5000, monitor_port=None, tunnel_key=None, config_file=None):
  """Starts the Cloudflare tunnel and returns the public URL."""
  binary_path = await ensure_binary()
  monitor_port = monitor_port or randint(8100, 9000)

  cmd = [binary_path, "tunnel", "--metrics", f"127.0.0.1:{monitor_port}"]

  if config_file:
    cmd += ["--config", config_file, "run"]
  elif tunnel_key:
    cmd += ["--url", f"http://127.0.0.1:{app_port}", "run", tunnel_key]
  else:
    cmd += ["--url", f"http://127.0.0.1:{app_port}"]

  try:
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
  except Exception as e:
    raise RuntimeError(f"Failed to start Cloudflare tunnel: {e}")

  atexit.register(process.terminate)

  monitor_url = f"http://127.0.0.1:{monitor_port}/metrics"

  for attempt in range(15):
    try:
      async with aiohttp.ClientSession() as session:
        async with session.get(monitor_url) as response:
          metrics = await response.text()
          if tunnel_key or config_file:
            if re.search(r"cloudflared_tunnel_ha_connections\s\d", metrics):
              return "Tunneled connection active"
          else:
            match = re.search(r"https?://[^\s]+.trycloudflare.com", metrics)
            if match:
              return match.group()
    except aiohttp.ClientError:
      await asyncio.sleep(2 ** attempt / 4)

  raise RuntimeError("! Unable to establish Cloudflare connection")