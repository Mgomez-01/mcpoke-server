#!/usr/bin/env python3
"""
API Function Extractor

This script analyzes the implementation plan and identifies all the
required API functions we'll need to implement.
"""

import os
import re
from typing import List, Dict, Any

def extract_commands_from_implementation_plan(plan_path: str) -> List[Dict[str, Any]]:
    """
    Extract MCP commands from the implementation plan.
    
    Args:
        plan_path: Path to the implementation plan file
    
    Returns:
        List of command information
    """
    commands = []
    
    with open(plan_path, 'r') as f:
        content = f.read()
    
    # Find all command examples
    command_blocks = re.findall(r'```json\s*(\{[\s\S]*?\})\s*```', content)
    
    for block in command_blocks:
        # Extract command name
        command_match = re.search(r'"command":\s*"([^"]+)"', block)
        if command_match:
            command_name = command_match.group(1)
            
            # Extract parameters
            params = {}
            param_matches = re.findall(r'"([^"]+)":\s*"?([^",}]+)"?', block)
            for key, value in param_matches:
                if key != "command":
                    params[key] = value
            
            # Add to commands list
            commands.append({
                "command": command_name,
                "parameters": params
            })
    
    return commands

def map_commands_to_api_calls(commands: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    """
    Map MCP commands to required PokéAPI calls.
    
    Args:
        commands: List of MCP commands
    
    Returns:
        Dictionary mapping commands to API calls
    """
    api_calls = {}
    
    for command in commands:
        command_name = command["command"]
        
        if command_name == "get_pokemon":
            api_calls[command_name] = [
                "pokemon/{name_or_id}",
                "pokemon-species/{name_or_id}",
                "evolution-chain/{id}"
            ]
        elif command_name == "search_pokemon":
            api_calls[command_name] = [
                "pokemon?limit={limit}"
            ]
        elif command_name == "get_ability":
            api_calls[command_name] = [
                "ability/{name_or_id}"
            ]
        elif command_name == "get_type":
            api_calls[command_name] = [
                "type/{name_or_id}"
            ]
        elif command_name == "get_move":
            api_calls[command_name] = [
                "move/{name_or_id}"
            ]
        elif command_name == "compare_pokemon":
            api_calls[command_name] = [
                "pokemon/{name_or_id} (for each Pokémon in the list)"
            ]
        elif command_name == "get_type_effectiveness":
            api_calls[command_name] = [
                "type/{attacking_type}",
                "type/{defending_type} (for each defending type)"
            ]
    
    return api_calls

def generate_api_functions_list(api_calls: Dict[str, List[str]], output_path: str) -> None:
    """
    Generate a list of required API functions.
    
    Args:
        api_calls: Dictionary mapping commands to API calls
        output_path: Path to the output file
    """
    with open(output_path, 'w') as f:
        f.write("# Required API Functions for MCPoke Server\n\n")
        f.write("This document lists all the API functions we need to implement for the MCPoke Server.\n\n")
        
        for command, calls in api_calls.items():
            f.write(f"## {command}\n\n")
            f.write("API calls:\n")
            for call in calls:
                f.write(f"- {call}\n")
            f.write("\n")
        
        f.write("\n## Summary of Required API Functions\n\n")
        
        # Collect unique API calls
        unique_calls = set()
        for calls in api_calls.values():
            for call in calls:
                unique_calls.add(call)
        
        # Group by endpoint
        endpoints = {}
        for call in unique_calls:
            endpoint = call.split('/')[0].split('?')[0]
            if endpoint not in endpoints:
                endpoints[endpoint] = []
            endpoints[endpoint].append(call)
        
        # Write summary
        for endpoint, calls in endpoints.items():
            f.write(f"### {endpoint}\n\n")
            for call in sorted(calls):
                f.write(f"- {call}\n")
            f.write("\n")
        
        # Implementation guidance
        f.write("\n## Implementation Notes\n\n")
        f.write("When implementing the API client, we should:\n\n")
        f.write("1. Create a base function for making API requests\n")
        f.write("2. Create specific functions for each endpoint\n")
        f.write("3. Implement proper error handling and retries\n")
        f.write("4. Use the cache to reduce API calls\n")
        f.write("5. Consider implementing pagination support for list endpoints\n")
        
        # Function stub examples
        f.write("\n## Function Stubs\n\n")
        f.write("```python\n")
        f.write("def make_request(endpoint: str, param: Optional[str] = None, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Make a request to the PokéAPI.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_pokemon(name_or_id: str) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch Pokémon data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_pokemon_species(name_or_id: str) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch Pokémon species data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_evolution_chain(chain_id: int) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch evolution chain data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_ability(name_or_id: str) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch ability data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_type(name_or_id: str) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch type data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_move(name_or_id: str) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch move data.\"\"\"\n")
        f.write("    pass\n\n")
        
        f.write("def fetch_all_pokemon(limit: int = 1000, offset: int = 0) -> Dict[str, Any]:\n")
        f.write("    \"\"\"Fetch all Pokémon (paginated).\"\"\"\n")
        f.write("    pass\n")
        f.write("```\n")

def main() -> None:
    """
    Main function.
    """
    print("API Function Extractor")
    print("=====================")
    
    # Paths
    plan_path = "../implementation_plan_readme.md"
    output_path = "api_functions.md"
    
    # Extract commands
    commands = extract_commands_from_implementation_plan(plan_path)
    print(f"Extracted {len(commands)} commands from the implementation plan.")
    
    # Map commands to API calls
    api_calls = map_commands_to_api_calls(commands)
    print(f"Mapped commands to API calls:")
    for command, calls in api_calls.items():
        print(f"- {command}: {len(calls)} API calls")
    
    # Generate API functions list
    generate_api_functions_list(api_calls, output_path)
    print(f"Generated API functions list: {output_path}")
    
    print("Done!")

if __name__ == "__main__":
    main()
