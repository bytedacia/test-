#!/usr/bin/env python3
"""
Discord Music Bot with Hidden Defense System
Setup script for easy installation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="discord-music-defense-bot",
    version="1.0.0",
    author="by_bytes",
    author_email="daciabyte@gmail.com",
    description="A sophisticated Discord music bot with hidden defense capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytedacia/test-",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "discord.py==2.3.2",
        "yt-dlp==2023.11.16",
        "spotipy==2.23.0",
        "google-generativeai==0.3.2",
        "python-dotenv==1.0.0",
        "PyNaCl==1.5.0",
        "aiohttp==3.9.1",
        "asyncio==3.4.3",
        "ffmpeg-python==0.2.0",
        "requests==2.31.0",
        "urllib3==2.0.7",
        "cryptography==41.0.7",
    ],
    entry_points={
        "console_scripts": [
            "discord-music-defense-bot=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.env.example"],
    },
)
