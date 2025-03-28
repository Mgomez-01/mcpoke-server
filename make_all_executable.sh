#!/bin/bash

# Make all scripts executable
cd "$(dirname "$0")"

# Make the top-level scripts executable
chmod +x generate_api_docs.sh

# Make the tools scripts executable
cd tools
chmod +x make_executables.sh
chmod +x api_explorer.py
chmod +x extract_api_functions.py
chmod +x generate_api_docs.py
chmod +x schema_analyzer.py
chmod +x run_api_explorer.sh
chmod +x run_doc_generator.sh

echo "All scripts are now executable."
