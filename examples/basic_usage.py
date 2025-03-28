#!/usr/bin/env python3
"""
Basic usage example for the MCPoke Server.

This script demonstrates how to interact with the MCPoke Server
using simple HTTP requests.
"""

import json
import requests

def make_mcp_request(command, **params):
    """
    Make a request to the MCPoke Server.
    
    Args:
        command: MCP command to execute
        **params: Additional parameters for the command
    
    Returns:
        Response from the server
    """
    # Combine command and parameters
    request_data = {
        "command": command,
        **params
    }
    
    # Send the request to the server
    response = requests.post(
        "http://localhost:8000",
        json=request_data
    )
    
    # Parse and return the response
    return response.json()

def main():
    """Run the example."""
    print("MCPoke Server Basic Usage Example")
    print("=================================")
    
    # Example 1: Get information about a Pokémon
    print("\n1. Getting information about Pikachu:")
    pikachu_info = make_mcp_request("get_pokemon", name_or_id="pikachu")
    print(f"Name: {pikachu_info['name']}")
    print(f"Types: {', '.join(pikachu_info['types'])}")
    print(f"Height: {pikachu_info['height']} m")
    print(f"Weight: {pikachu_info['weight']} kg")
    print(f"Description: {pikachu_info['description']}")
    
    # Example 2: Search for Pokémon
    print("\n2. Searching for Pokémon with 'char' in their name:")
    char_pokemon = make_mcp_request("search_pokemon", query="char", limit=3)
    for pokemon in char_pokemon:
        print(f"- {pokemon['name']} (ID: {pokemon['id']}, Types: {', '.join(pokemon['types'])})")
    
    # Example 3: Get ability information
    print("\n3. Getting information about the 'Blaze' ability:")
    blaze_info = make_mcp_request("get_ability", name_or_id="blaze")
    print(f"Name: {blaze_info['name']}")
    print(f"Effect: {blaze_info['effect']}")
    print(f"Pokémon with this ability: {', '.join(blaze_info['pokemon'][:5])}...")
    
    # Example 4: Get type effectiveness
    print("\n4. Calculating type effectiveness:")
    effectiveness = make_mcp_request(
        "get_type_effectiveness",
        attacking_type="electric",
        defending_types=["water", "flying"]
    )
    print(f"Electric vs Water/Flying: {effectiveness['effectiveness']}x damage ({effectiveness['description']})")

if __name__ == "__main__":
    main()
