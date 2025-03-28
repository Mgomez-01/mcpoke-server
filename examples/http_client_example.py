#!/usr/bin/env python3
"""
Example HTTP MCP client for MCPoke Server.

This script demonstrates how to use the MCPoke Server with an HTTP MCP client.
"""

import json
import sys
import uuid
import requests
from typing import Dict, Any, Optional

class MCPokeHttpClient:
    """HTTP client for the MCPoke Server."""
    
    def __init__(self, server_url="http://localhost:8000"):
        """
        Initialize the HTTP client.
        
        Args:
            server_url: URL of the MCPoke Server
        """
        self.server_url = server_url
        self.session_id = str(uuid.uuid4())
        # Track whether we're initialized
        self.initialized = False
        # Create a requests session to maintain cookies
        self.session = requests.Session()
        # Add a cookie with our session ID
        self.session.cookies.set("mcp_session_id", self.session_id)
    
    def send_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a JSON-RPC request to the MCPoke Server.
        
        Args:
            method: Method name
            params: Method parameters
        
        Returns:
            Response data
        """
        # Add session ID to params if it's not a special method
        actual_params = params.copy() if params else {}
        if method not in ["initialize", "shutdown"]:
            actual_params["session_id"] = self.session_id
            
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": actual_params,
            "id": str(uuid.uuid4())
        }
        
        print(f"Sending request: {json.dumps(request)}")
        
        try:
            # Add session ID in header as well
            headers = {"X-MCP-Session-ID": self.session_id}
            
            response = self.session.post(self.server_url, json=request, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            
            if "error" in result:
                print(f"Error: {result['error']['message']}")
                return {}
            
            print(f"Received response: {json.dumps(result)}")
            
            # Mark as initialized if this was an initialization request
            if method == "initialize":
                self.initialized = True
            
            return result.get("result", {})
        except Exception as e:
            print(f"Error: {str(e)}")
            return {}
    
    def initialize(self) -> Dict[str, Any]:
        """
        Initialize the MCP session.
        
        Returns:
            Initialization result
        """
        return self.send_request("initialize", {
            "session_id": self.session_id,
            "capabilities": {
                "core": {
                    "version": "1.0"
                },
                "tools": {
                    "version": "1.0"
                }
            }
        })
    
    def list_tools(self) -> Dict[str, Any]:
        """
        List available tools.
        
        Returns:
            Tools list
        """
        return self.send_request("listTools")
    
    def get_pokemon(self, name_or_id: str) -> Dict[str, Any]:
        """
        Get information about a Pokémon.
        
        Args:
            name_or_id: Name or ID of the Pokémon
        
        Returns:
            Pokémon information
        """
        return self.send_request("invokeTools.pokemon", {
            "action": "get_pokemon",
            "name_or_id": name_or_id
        })
    
    def search_pokemon(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search for Pokémon by name.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
        
        Returns:
            Search results
        """
        return self.send_request("invokeTools.pokemon", {
            "action": "search_pokemon",
            "query": query,
            "limit": limit
        })
    
    def shutdown(self) -> Dict[str, Any]:
        """
        Shut down the MCP session.
        
        Returns:
            Shutdown result
        """
        return self.send_request("shutdown", {
            "session_id": self.session_id
        })

def main():
    """Main entry point."""
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='MCPoke HTTP client example')
    parser.add_argument('--server', type=str, default='http://localhost:8000',
                       help='MCPoke Server URL (default: http://localhost:8000)')
    args = parser.parse_args()
    
    # Create client
    client = MCPokeHttpClient(args.server)
    
    # Initialize MCP session
    print("\n=== Initializing MCP Session ===")
    init_result = client.initialize()
    print(f"Server info: {init_result.get('server', {})}")
    print(f"Capabilities: {json.dumps(init_result.get('capabilities', {}), indent=2)}")
    
    # List available tools
    print("\n=== Available Tools ===")
    tools_result = client.list_tools()
    for tool in tools_result.get('tools', []):
        print(f"- {tool.get('name')}: {tool.get('description')}")
    
    # Example: Get a Pokémon
    print("\n=== Getting Pokémon: Pikachu ===")
    pokemon_result = client.get_pokemon("pikachu")
    if pokemon_result:
        print(f"Name: {pokemon_result.get('name')}")
        print(f"Types: {', '.join(pokemon_result.get('types', []))}")
        print(f"Abilities: {', '.join([a.get('name') for a in pokemon_result.get('abilities', [])])}")
        print(f"Height: {pokemon_result.get('height')} m")
        print(f"Weight: {pokemon_result.get('weight')} kg")
        
        stats = pokemon_result.get('stats', {})
        print("Stats:")
        for stat, value in stats.items():
            print(f"  {stat}: {value}")
    
    # Example: Search for Pokémon
    print("\n=== Searching for Pokémon: 'char' ===")
    search_result = client.search_pokemon("char", 3)
    for pokemon in search_result.get('results', []):
        print(f"- {pokemon.get('name')} (#{pokemon.get('id')}): {', '.join(pokemon.get('types', []))}")
    
    # Shut down MCP session
    print("\n=== Shutting Down MCP Session ===")
    shutdown_result = client.shutdown()
    print(f"Shutdown result: {shutdown_result}")

if __name__ == "__main__":
    main()
