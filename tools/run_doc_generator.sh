#!/bin/bash

# Run the API documentation generator
cd "$(dirname "$0")"
python3 generate_api_docs.py
