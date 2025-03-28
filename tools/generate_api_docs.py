#!/usr/bin/env python3
"""
API Documentation Generator

This script runs both the API Explorer and the API Function Extractor
to generate comprehensive API documentation for the MCPoke Server.
"""

import os
import subprocess
import time

def run_command(command):
    """Run a shell command and return the output."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    
    return process.returncode, stdout, stderr

def main():
    """Main function."""
    print("API Documentation Generator")
    print("==========================")
    
    # Create the output directory
    os.makedirs("api_docs", exist_ok=True)
    
    # Step 1: Extract API functions from the implementation plan
    print("\nStep 1: Extracting API functions from the implementation plan...")
    returncode, stdout, stderr = run_command("python3 extract_api_functions.py")
    if returncode != 0:
        print("Error running extract_api_functions.py:")
        print(stderr)
        return
    
    print(stdout)
    
    # Step 2: Run the API Explorer
    print("\nStep 2: Running the API Explorer...")
    returncode, stdout, stderr = run_command("python3 api_explorer.py")
    if returncode != 0:
        print("Error running api_explorer.py:")
        print(stderr)
        return
    
    print(stdout)
    
    # Step 3: Run the Schema Analyzer
    print("\nStep 3: Running the Schema Analyzer...")
    returncode, stdout, stderr = run_command("python3 schema_analyzer.py")
    if returncode != 0:
        print("Error running schema_analyzer.py:")
        print(stderr)
        # Continue anyway, this is not a critical error
    else:
        print(stdout)
    
    # Step 4: Combine the documentation
    print("\nStep 4: Combining documentation...")
    
    # Move and rename the files
    os.makedirs("api_docs/samples", exist_ok=True)
    os.makedirs("api_docs/schemas", exist_ok=True)
    
    # Copy API functions list
    returncode, stdout, stderr = run_command("cp api_functions.md api_docs/")
    if returncode != 0:
        print("Error copying api_functions.md:")
        print(stderr)
    
    # Copy API reference
    returncode, stdout, stderr = run_command("cp api_samples/api_reference.md api_docs/")
    if returncode != 0:
        print("Error copying api_reference.md:")
        print(stderr)
    
    # Copy API samples
    returncode, stdout, stderr = run_command("cp api_samples/*.json api_docs/samples/")
    if returncode != 0:
        print("Error copying API samples:")
        print(stderr)
    
    # Copy schemas
    returncode, stdout, stderr = run_command("cp -r api_docs/schemas/* api_docs/schemas/")
    if returncode != 0:
        print("Error copying schemas:")
        print(stderr)
    
    # Create a README.md
    with open("api_docs/README.md", "w") as f:
        f.write("# MCPoke Server API Documentation\n\n")
        f.write("This directory contains comprehensive documentation of the PokéAPI endpoints used in the MCPoke Server.\n\n")
        f.write("## Contents\n\n")
        f.write("- [API Functions](api_functions.md) - List of all API functions needed for the MCPoke Server\n")
        f.write("- [API Reference](api_reference.md) - Reference of all PokéAPI endpoints used\n")
        f.write("- [Samples](samples/) - Sample responses from the PokéAPI\n")
        f.write("- [Schemas](schemas/) - TypeScript interfaces and JSON Schemas for API responses\n\n")
        f.write("## How to Use This Documentation\n\n")
        f.write("1. Start by reading the **API Functions** document to understand what API functions we need to implement.\n")
        f.write("2. Refer to the **API Reference** for details on how to call each endpoint.\n")
        f.write("3. Look at the **Samples** to understand the structure of the API responses.\n")
        f.write("4. Use the **Schemas** as a reference for response data structures in your implementation.\n\n")
        f.write("## Implementation Strategy\n\n")
        f.write("Based on this documentation, we should implement the following components:\n\n")
        f.write("1. A generic API client that can make requests to any PokéAPI endpoint.\n")
        f.write("2. Specific functions for each endpoint we need to use.\n")
        f.write("3. A caching layer to reduce API calls.\n")
        f.write("4. Data processors to transform the API responses into the format expected by our MCP functions.\n")
    
    # Create an API endpoints cheat sheet
    with open("api_docs/api_endpoints_cheatsheet.md", "w") as f:
        f.write("# PokéAPI Endpoints Cheat Sheet\n\n")
        f.write("Quick reference for PokéAPI endpoints used in the MCPoke Server.\n\n")
        
        f.write("## Main Endpoints\n\n")
        f.write("| Endpoint | Description | URL Pattern |\n")
        f.write("|----------|-------------|------------|\n")
        f.write("| Pokémon | Get basic Pokémon data | `/pokemon/{name_or_id}` |\n")
        f.write("| Pokémon Species | Get Pokémon species data | `/pokemon-species/{name_or_id}` |\n")
        f.write("| Evolution Chain | Get evolution chain | `/evolution-chain/{id}` |\n")
        f.write("| Type | Get type data | `/type/{name_or_id}` |\n")
        f.write("| Ability | Get ability data | `/ability/{name_or_id}` |\n")
        f.write("| Move | Get move data | `/move/{name_or_id}` |\n\n")
        
        f.write("## List Endpoints\n\n")
        f.write("| Endpoint | Description | URL Pattern |\n")
        f.write("|----------|-------------|------------|\n")
        f.write("| Pokémon List | Get a list of all Pokémon | `/pokemon?limit={limit}&offset={offset}` |\n")
        f.write("| Type List | Get a list of all types | `/type?limit={limit}&offset={offset}` |\n")
        f.write("| Ability List | Get a list of all abilities | `/ability?limit={limit}&offset={offset}` |\n")
        f.write("| Move List | Get a list of all moves | `/move?limit={limit}&offset={offset}` |\n")
    
    print("\nAll documentation has been generated and combined in the api_docs directory.")
    print("You can find the following files:")
    print("- api_docs/README.md")
    print("- api_docs/api_functions.md")
    print("- api_docs/api_reference.md")
    print("- api_docs/api_endpoints_cheatsheet.md")
    print("- api_docs/samples/*.json")
    print("- api_docs/schemas/*.ts")
    print("- api_docs/schemas/*.schema.json")

if __name__ == "__main__":
    main()
