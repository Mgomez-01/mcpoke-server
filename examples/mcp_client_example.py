#!/usr/bin/env python3
"""
Example MCP client for MCPoke Server.

This script demonstrates how to use the MCPoke Server with a simple MCP client.
"""

import json
import sys
import uuid
from typing import Dict, Any, Optional

def send_request(method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Send a JSON-RPC request to the MCPoke Server.
    
    Args:
        method: Method name
        params: Method parameters
    
    Returns:
        Response data
    """
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": str(uuid.uuid4())
    }
    
    # Send request to stderr for debugging
    print(f"Sending request: {json.dumps(request)}", file=sys.stderr)
    
    # Send request to stdout
    print(json.dumps(request))
    sys.stdout.flush()
    
    # Read response from stdin
    response_data = sys.stdin.readline().strip()
    
    try:
        response = json.loads(response_data)
        
        if "error" in response:
            print(f"Error: {response['error']['message']}", file=sys.stderr)
            return {}
        
        # Send response to stderr for debugging
        print(f"Received response: {json.dumps(response)}", file=sys.stderr)
        
        return response.get("result", {})
    except json.JSONDecodeError:
        print(f"Error: Could not parse response: {response_data}", file=sys.stderr)
        return {}

def initialize() -> Dict[str, Any]:
    """
    Initialize the MCP session.
    
    Returns:
        Initialization result
    """
    return send_request("initialize", {
        "capabilities": {
            "core": {
                "version": "1.0"
            },
            "tools": {
                "version": "1.0"
            }
        }
    })

def list_tools() -> Dict[str, Any]:
    """
    List available tools.
    
    Returns:
        Tools list
    """
    return send_request("listTools")

def get_pokemon(name_or_id: str) -> Dict[str, Any]:
    """
    Get information about a Pokémon.
    
    Args:
        name_or_id: Name or ID of the Pokémon
    
    Returns:
        Pokémon information
    """
    return send_request("invokeTools.pokemon", {
        "action": "get_pokemon",
        "name_or_id": name_or_id
    })

def search_pokemon(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search for Pokémon by name.
    
    Args:
        query: Search query
        limit: Maximum number of results to return
    
    Returns:
        Search results
    """
    return send_request("invokeTools.pokemon", {
        "action": "search_pokemon",
        "query": query,
        "limit": limit
    })

def get_ability(name_or_id: str) -> Dict[str, Any]:
    """
    Get information about an ability.
    
    Args:
        name_or_id: Name or ID of the ability
    
    Returns:
        Ability information
    """
    return send_request("invokeTools.pokemon", {
        "action": "get_ability",
        "name_or_id": name_or_id
    })

def get_type(name_or_id: str) -> Dict[str, Any]:
    """
    Get information about a type.
    
    Args:
        name_or_id: Name or ID of the type
    
    Returns:
        Type information
    """
    return send_request("invokeTools.pokemon", {
        "action": "get_type",
        "name_or_id": name_or_id
    })

def get_move(name_or_id: str) -> Dict[str, Any]:
    """
    Get information about a move.
    
    Args:
        name_or_id: Name or ID of the move
    
    Returns:
        Move information
    """
    return send_request("invokeTools.pokemon", {
        "action": "get_move",
        "name_or_id": name_or_id
    })

def compare_pokemon(pokemon_list: list) -> Dict[str, Any]:
    """
    Compare multiple Pokémon.
    
    Args:
        pokemon_list: List of Pokémon names or IDs
    
    Returns:
        Comparison results
    """
    return send_request("invokeTools.pokemon", {
        "action": "compare_pokemon",
        "pokemon_list": pokemon_list
    })

def get_type_effectiveness(attacking_type: str, defending_types: list) -> Dict[str, Any]:
    """
    Calculate type effectiveness.
    
    Args:
        attacking_type: Attacking type
        defending_types: List of defending types
    
    Returns:
        Type effectiveness information
    """
    return send_request("invokeTools.pokemon", {
        "action": "get_type_effectiveness",
        "attacking_type": attacking_type,
        "defending_types": defending_types
    })

def shutdown() -> Dict[str, Any]:
    """
    Shut down the MCP session.
    
    Returns:
        Shutdown result
    """
    return send_request("shutdown")

def main():
    """Main entry point."""
    # Initialize MCP session
    init_result = initialize()
    print(f"Initialized MCP session: {json.dumps(init_result, indent=2)}", file=sys.stderr)
    
    # List available tools
    tools_result = list_tools()
    print(f"Available tools: {json.dumps(tools_result, indent=2)}", file=sys.stderr)
    
    # Example: Get a Pokémon
    pokemon_result = get_pokemon("pikachu")
    print(f"Pikachu information: {json.dumps(pokemon_result, indent=2)}", file=sys.stderr)
    
    # Example: Search for Pokémon
    search_result = search_pokemon("char", 3)
    print(f"Search results: {json.dumps(search_result, indent=2)}", file=sys.stderr)
    
    # Example: Get an ability
    ability_result = get_ability("static")
    print(f"Static ability information: {json.dumps(ability_result, indent=2)}", file=sys.stderr)
    
    # Example: Get a type
    type_result = get_type("electric")
    print(f"Electric type information: {json.dumps(type_result, indent=2)}", file=sys.stderr)
    
    # Example: Get a move
    move_result = get_move("thunderbolt")
    print(f"Thunderbolt move information: {json.dumps(move_result, indent=2)}", file=sys.stderr)
    
    # Example: Compare Pokémon
    compare_result = compare_pokemon(["pikachu", "bulbasaur"])
    print(f"Comparison results: {json.dumps(compare_result, indent=2)}", file=sys.stderr)
    
    # Example: Calculate type effectiveness
    effectiveness_result = get_type_effectiveness("electric", ["water", "ground"])
    print(f"Type effectiveness: {json.dumps(effectiveness_result, indent=2)}", file=sys.stderr)
    
    # Shut down MCP session
    shutdown_result = shutdown()
    print(f"Shut down MCP session: {json.dumps(shutdown_result, indent=2)}", file=sys.stderr)

if __name__ == "__main__":
    main()
