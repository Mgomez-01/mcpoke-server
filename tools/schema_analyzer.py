#!/usr/bin/env python3
"""
PokéAPI Schema Analyzer

This script analyzes the PokéAPI response schemas and generates
TypeScript/JSON Schema definitions for better documentation.
"""

import json
import os
import re
from typing import Dict, Any, List, Union, Optional

def infer_type(value: Any) -> str:
    """
    Infer the TypeScript type of a value.
    
    Args:
        value: Value to infer the type of
    
    Returns:
        TypeScript type
    """
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "number"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, list):
        if not value:
            return "any[]"
        
        # Get the type of the first item
        item_type = infer_type(value[0])
        
        # Check if all items have the same type
        for item in value[1:]:
            if infer_type(item) != item_type:
                return "any[]"
        
        return f"{item_type}[]"
    elif isinstance(value, dict):
        return "object"
    else:
        return "any"

def generate_typescript_interface(data: Dict[str, Any], name: str, indent: str = "  ") -> str:
    """
    Generate a TypeScript interface from a dictionary.
    
    Args:
        data: Dictionary to generate an interface from
        name: Name of the interface
        indent: Indentation string
    
    Returns:
        TypeScript interface
    """
    result = f"interface {name} {{\n"
    
    for key, value in data.items():
        # Convert snake_case to camelCase for TypeScript
        ts_key = key
        if "_" in key:
            parts = key.split("_")
            ts_key = parts[0] + "".join(part.capitalize() for part in parts[1:])
        
        ts_type = infer_type(value)
        
        if ts_type == "object" and isinstance(value, dict):
            sub_name = f"{name}{key.capitalize()}"
            result += f"{indent}{ts_key}: {sub_name};\n"
        else:
            result += f"{indent}{ts_key}: {ts_type};\n"
    
    result += "}"
    
    # Process nested objects
    for key, value in data.items():
        if infer_type(value) == "object" and isinstance(value, dict):
            sub_name = f"{name}{key.capitalize()}"
            result += "\n\n" + generate_typescript_interface(value, sub_name, indent)
    
    return result

def generate_json_schema(data: Dict[str, Any], name: str) -> Dict[str, Any]:
    """
    Generate a JSON Schema from a dictionary.
    
    Args:
        data: Dictionary to generate a schema from
        name: Name of the schema
    
    Returns:
        JSON Schema
    """
    properties = {}
    required = []
    
    for key, value in data.items():
        prop_type = infer_type(value)
        
        if prop_type == "null":
            properties[key] = {"type": "null"}
        elif prop_type == "boolean":
            properties[key] = {"type": "boolean"}
        elif prop_type == "number":
            properties[key] = {"type": "number"}
        elif prop_type == "string":
            properties[key] = {"type": "string"}
        elif prop_type.endswith("[]"):
            item_type = prop_type[:-2]
            if item_type == "object" and isinstance(value[0], dict):
                item_schema = generate_json_schema(value[0], f"{name}{key.capitalize()}Item")
                properties[key] = {
                    "type": "array",
                    "items": item_schema
                }
            else:
                properties[key] = {
                    "type": "array",
                    "items": {"type": item_type}
                }
        elif prop_type == "object":
            properties[key] = generate_json_schema(value, f"{name}{key.capitalize()}")
        else:
            properties[key] = {"type": "any"}
        
        # Assume all properties are required
        required.append(key)
    
    return {
        "type": "object",
        "properties": properties,
        "required": required,
        "additionalProperties": False
    }

def analyze_sample_file(file_path: str) -> Dict[str, Any]:
    """
    Analyze a sample API response file.
    
    Args:
        file_path: Path to the sample file
    
    Returns:
        Analysis results
    """
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract the JSON part
    json_match = re.search(r'(\{[\s\S]*\})', content)
    if not json_match:
        return {"error": "No JSON found in the file"}
    
    json_str = json_match.group(1)
    
    # Parse the JSON
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": f"Failed to parse JSON: {e}"}
    
    # Generate a TypeScript interface name
    filename = os.path.basename(file_path)
    interface_name = re.sub(r'[^a-zA-Z0-9_]', '', filename.split('.')[0].title()) + "Response"
    
    # Generate a TypeScript interface
    typescript_interface = generate_typescript_interface(data, interface_name)
    
    # Generate a JSON Schema
    json_schema = generate_json_schema(data, interface_name)
    
    return {
        "interface_name": interface_name,
        "typescript_interface": typescript_interface,
        "json_schema": json_schema
    }

def main() -> None:
    """
    Main function.
    """
    print("PokéAPI Schema Analyzer")
    print("======================")
    
    # Find all sample files
    sample_dir = "api_samples"
    sample_files = [f for f in os.listdir(sample_dir) if f.endswith(".json")]
    
    if not sample_files:
        print(f"No sample files found in {sample_dir}. Run api_explorer.py first.")
        return
    
    # Create the output directory
    output_dir = "api_docs/schemas"
    os.makedirs(output_dir, exist_ok=True)
    
    # Analyze each sample file
    results = {}
    for file in sample_files:
        print(f"Analyzing {file}...")
        file_path = os.path.join(sample_dir, file)
        result = analyze_sample_file(file_path)
        if "error" in result:
            print(f"  Error: {result['error']}")
            continue
        
        results[file] = result
        
        # Save the TypeScript interface
        ts_file = os.path.splitext(file)[0] + ".ts"
        with open(os.path.join(output_dir, ts_file), 'w') as f:
            f.write("/**\n")
            f.write(f" * TypeScript interface for {file}\n")
            f.write(" * Generated by PokéAPI Schema Analyzer\n")
            f.write(" */\n\n")
            f.write(result["typescript_interface"])
            f.write("\n")
        
        # Save the JSON Schema
        schema_file = os.path.splitext(file)[0] + ".schema.json"
        with open(os.path.join(output_dir, schema_file), 'w') as f:
            json.dump(result["json_schema"], f, indent=2)
    
    # Generate an index file
    with open(os.path.join(output_dir, "index.md"), 'w') as f:
        f.write("# PokéAPI Schemas\n\n")
        f.write("This directory contains TypeScript interfaces and JSON Schemas for PokéAPI responses.\n\n")
        f.write("## TypeScript Interfaces\n\n")
        for file, result in results.items():
            ts_file = os.path.splitext(file)[0] + ".ts"
            f.write(f"- [{result['interface_name']}]({ts_file})\n")
        
        f.write("\n## JSON Schemas\n\n")
        for file, result in results.items():
            schema_file = os.path.splitext(file)[0] + ".schema.json"
            f.write(f"- [{result['interface_name']}]({schema_file})\n")
    
    print(f"\nGenerated TypeScript interfaces and JSON Schemas for {len(results)} sample files.")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    main()
