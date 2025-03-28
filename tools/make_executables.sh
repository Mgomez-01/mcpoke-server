#!/bin/bash

# Make all scripts executable
cd "$(dirname "$0")"
chmod +x api_explorer.py
chmod +x extract_api_functions.py
chmod +x generate_api_docs.py
chmod +x schema_analyzer.py
chmod +x run_api_explorer.sh
chmod +x run_doc_generator.sh
chmod +x make_executables.sh

echo "All scripts are now executable."
