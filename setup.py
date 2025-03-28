#!/usr/bin/env python3
"""
Setup script for the MCPoke Server.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="mcpoke-server",
    version="0.1.0",
    author="MCPoke Server Contributors",
    author_email="example@example.com",
    description="A Model Context Protocol (MCP) server for Pokémon API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/mcpoke-server",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mcpoke-server=mcpoke_server:main",
        ],
    },
)
