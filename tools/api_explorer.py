#!/usr/bin/env python3
"""
PokéAPI Explorer

This script explores the PokéAPI endpoints and saves sample responses
for reference. It helps us understand the API structure and plan our
implementation accordingly.
"""

import json
import os
import requests
import time
from typing import Dict, Any, List, Optional

# Configuration
BASE_URL = "https://pokeapi.co/api/v2"
OUTPUT_DIR = "api_samples"
REQUEST_DELAY = 1.0  # Delay between requests to avoid hitting rate limits

# Endpoints to explore with sample IDs/names
ENDPOINTS = [
    # Pokémon endpoints
    {"endpoint": "pokemon", "param": "pikachu", "description": "Get basic Pokémon data"},
    {"endpoint": "pokemon", "param": "charizard", "description": "Get basic Pokémon data (another example)"},
    {"endpoint": "pokemon-species", "param": "pikachu", "description": "Get Pokémon species data (descriptions, etc.)"},
    {"endpoint": "pokemon-species", "param": "eevee", "description": "Get Pokémon species with multiple evolutions"},
    {"endpoint": "evolution-chain", "param": "67", "description": "Get Eevee's evolution chain"},
    {"endpoint": "evolution-chain", "param": "10", "description": "Get Pichu-Pikachu-Raichu evolution chain"},
    
    # Type endpoints
    {"endpoint": "type", "param": "electric", "description": "Get electric type data"},
    {"endpoint": "type", "param": "water", "description": "Get water type data"},
    {"endpoint": "type", "param": "fire", "description": "Get fire type data"},
    
    # Ability endpoints
    {"endpoint": "ability", "param": "static", "description": "Get Static ability data"},
    {"endpoint": "ability", "param": "blaze", "description": "Get Blaze ability data"},
    {"endpoint": "ability", "param": "intimidate", "description": "Get Intimidate ability data"},
    
    # Move endpoints
    {"endpoint": "move", "param": "thunderbolt", "description": "Get Thunderbolt move data"},
    {"endpoint": "move", "param": "surf", "description": "Get Surf move data"},
    {"endpoint": "move", "param": "flamethrower", "description": "Get Flamethrower move data"},
    
    # List endpoints (for search functionality)
    {"endpoint": "pokemon", "description": "List all Pokémon (paginated)"},
    {"endpoint": "type", "description": "List all types"},
    {"endpoint": "ability", "description": "List all abilities"},
    {"endpoint": "move", "description": "List all moves"},
]

def make_request(endpoint: str, param: Optional[str] = None) -> Dict[str, Any]:
    """
    Make a request to the PokéAPI.
    
    Args:
        endpoint: API endpoint
        param: Optional parameter (ID or name)
    
    Returns:
        API response data
    """
    url = f"{BASE_URL}/{endpoint}"
    if param is not None:
        url = f"{url}/{param}"
    
    print(f"Requesting: {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def save_response(endpoint: str, param: Optional[str], data: Dict[str, Any], description: str) -> None:
    """
    Save the API response to a file.
    
    Args:
        endpoint: API endpoint
        param: Optional parameter (ID or name)
        data: API response data
        description: Description of the endpoint
    """
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate a filename
    filename = f"{endpoint}"
    if param is not None:
        filename = f"{filename}_{param}"
    filename = f"{filename}.json"
    
    # Save the data
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(f"// {description}\n")
        f.write(f"// Endpoint: {BASE_URL}/{endpoint}")
        if param is not None:
            f.write(f"/{param}")
        f.write("\n\n")
        json.dump(data, f, indent=2)
    
    print(f"Saved to: {filepath}")

def generate_api_reference() -> None:
    """
    Generate an API reference document based on the saved responses.
    """
    reference_path = os.path.join(OUTPUT_DIR, "api_reference.md")
    
    with open(reference_path, 'w') as f:
        f.write("# PokéAPI Reference\n\n")
        f.write("This document provides a reference for the PokéAPI endpoints used in the MCPoke Server.\n\n")
        
        # Group endpoints by type
        endpoint_groups = {
            "pokemon": [],
            "pokemon-species": [],
            "evolution-chain": [],
            "type": [],
            "ability": [],
            "move": [],
        }
        
        for endpoint_info in ENDPOINTS:
            endpoint = endpoint_info["endpoint"]
            if endpoint in endpoint_groups:
                endpoint_groups[endpoint].append(endpoint_info)
        
        # Write each section
        for group_name, endpoints in endpoint_groups.items():
            if not endpoints:
                continue
                
            f.write(f"## {group_name.title()} Endpoints\n\n")
            
            for endpoint_info in endpoints:
                f.write(f"### {endpoint_info['description']}\n\n")
                f.write("```\n")
                f.write(f"GET {BASE_URL}/{endpoint_info['endpoint']}")
                if "param" in endpoint_info:
                    f.write(f"/{endpoint_info['param']}")
                f.write("\n```\n\n")
                
                # Add a note about the sample file
                filename = f"{endpoint_info['endpoint']}"
                if "param" in endpoint_info:
                    filename = f"{filename}_{endpoint_info['param']}"
                filename = f"{filename}.json"
                
                f.write(f"Sample response: `{filename}`\n\n")
                
                # Add a separator
                f.write("---\n\n")
        
        f.write("\n\n## Usage in MCPoke Server\n\n")
        f.write("These endpoints will be used in the MCPoke Server as follows:\n\n")
        
        f.write("1. **Get Pokémon Information**:\n")
        f.write("   - Fetch basic data with `pokemon/{name}`\n")
        f.write("   - Fetch species data with `pokemon-species/{name}`\n")
        f.write("   - Fetch evolution chain using the URL from species data\n\n")
        
        f.write("2. **Search Pokémon**:\n")
        f.write("   - Fetch the list of all Pokémon with `pokemon?limit=1000`\n")
        f.write("   - Filter the results by name on the client side\n\n")
        
        f.write("3. **Get Ability Information**:\n")
        f.write("   - Fetch ability data with `ability/{name}`\n\n")
        
        f.write("4. **Get Type Information**:\n")
        f.write("   - Fetch type data with `type/{name}`\n\n")
        
        f.write("5. **Get Move Information**:\n")
        f.write("   - Fetch move data with `move/{name}`\n\n")
        
        f.write("6. **Calculate Type Effectiveness**:\n")
        f.write("   - Use the damage relations from `type/{name}` for both attacking and defending types\n\n")
        
        f.write("7. **Compare Pokémon**:\n")
        f.write("   - Fetch data for multiple Pokémon and compare their stats and types\n")
    
    print(f"Generated API reference: {reference_path}")

def main() -> None:
    """
    Main function.
    """
    print("PokéAPI Explorer")
    print("===============")
    
    # Explore each endpoint
    for endpoint_info in ENDPOINTS:
        endpoint = endpoint_info["endpoint"]
        param = endpoint_info.get("param")
        description = endpoint_info["description"]
        
        try:
            # Make the request
            data = make_request(endpoint, param)
            
            # Save the response
            save_response(endpoint, param, data, description)
            
            # Delay to avoid hitting rate limits
            time.sleep(REQUEST_DELAY)
        except Exception as e:
            print(f"Error exploring {endpoint}/{param}: {e}")
    
    # Generate API reference
    generate_api_reference()
    
    print("Done!")

if __name__ == "__main__":
    main()
