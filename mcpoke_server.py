#!/usr/bin/env python3
"""
MCPoke Server - A Model Context Protocol (MCP) server for Pokémon API

This is the main entry point for the MCPoke Server, which provides a bridge between
MCP-compatible AI models (like Claude) and the PokéAPI.
"""

import argparse
import json
import os
import sys
from src.server import MCPokeServer

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='MCPoke Server - MCP server for Pokémon API')
    parser.add_argument('--config', type=str, default='config.json',
                        help='Path to the configuration file')
    parser.add_argument('--host', type=str,
                        help='Host address to bind the server to')
    parser.add_argument('--port', type=int,
                        help='Port to run the server on')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug mode')
    return parser.parse_args()

def load_config(config_path):
    """Load configuration from the specified JSON file."""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Config file {config_path} not found. Using default configuration.")
            return {
                "server": {
                    "host": "0.0.0.0",
                    "port": 8000,
                    "debug": False
                },
                "api": {
                    "base_url": "https://pokeapi.co/api/v2",
                    "timeout": 10
                },
                "cache": {
                    "enabled": True,
                    "ttl": 86400,
                    "max_size": 1000
                }
            }
    except Exception as e:
        print(f"Failed to load config: {e}")
        sys.exit(1)

def main():
    """Main entry point for the MCPoke Server."""
    args = parse_args()
    config = load_config(args.config)
    
    # Override config with command-line arguments
    if args.host:
        config["server"]["host"] = args.host
    if args.port:
        config["server"]["port"] = args.port
    if args.debug:
        config["server"]["debug"] = True
    
    # Create and start the MCPoke Server
    server = MCPokeServer(config)
    server.start()

if __name__ == "__main__":
    main()
