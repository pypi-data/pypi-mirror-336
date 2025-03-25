# Cloudflarify

A Python package to easily **start and manage Cloudflare Tunnels** for exposing local services securely.

## Features

✅ **Auto-downloads & updates** the `cloudflared` binary  
✅ **Supports Windows, Linux, and macOS**  
✅ **Works with Cloudflare account tunnels or TryCloudflare**  
✅ **Asynchronous & efficient (`aiohttp` based)**  
✅ **Automatic exponential backoff for stable connections**  

## Installation

Install via PyPI:

```bash
pip install cloudflarify
```

## Usage

### Basic Usage (TryCloudflare)

```python
import asyncio
from cloudflarify import start_tunnel

async def main():
    tunnel_url = await start_tunnel(app_port=5000)
    print(f"Tunnel is live at: {tunnel_url}")

asyncio.run(main())
```

### With Cloudflare Account Tunnel

```python
asyncio.run(start_tunnel(app_port=5000, tunnel_key="YOUR_TUNNEL_KEY"))
```

### Using a Config File

```python
asyncio.run(start_tunnel(config_file="path/to/config.yml"))
```

### Running a Flask App with Cloudflare Tunnel

```python
from flask import Flask
import asyncio
from cloudflarify import start_tunnel

port = 5000
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Cloudflare Tunnel!"

if __name__ == "__main__":
    asyncio.run(start_tunnel(app_port=port))  # Start tunnel
    app.run(port=port)  # Start Flask app
```

## Requirements

- Python 3.7+
- `aiohttp`, `tqdm`

## Acknowledgement

This project was inspired by [flask-cloudflared](https://github.com/UWUplus/flask-cloudflared).  

## License

This project is MIT licensed.
