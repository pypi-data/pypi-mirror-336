from setuptools import setup, find_packages

setup(
  name="cloudflarify",
  version="1.0.0",
  author="JOBIANS TECHIE",
  author_email="jobianstechie@gmail.com",
  description="A Python wrapper to run Cloudflare tunnels programmatically",
  long_description=open("README.md").read(),
  long_description_content_type="text/markdown",
  url="https://github.com/Jobians/cloudflarify",
  packages=find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires=">=3.7",
  install_requires=[
    "aiohttp",
    "tqdm"
  ],
)