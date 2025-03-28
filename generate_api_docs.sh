#!/bin/bash

# Run the API documentation generator from the main directory
cd "$(dirname "$0")"
cd tools
./make_executables.sh
./run_doc_generator.sh

# Copy the output to the main directory
mkdir -p ../api_docs
cp -r api_docs/* ../api_docs/

echo "API documentation has been generated in the api_docs directory."
