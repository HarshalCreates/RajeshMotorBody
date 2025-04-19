#!/usr/bin/env bash
# Exit on error
set -o errexit

# Create an upload folder if it doesn't exist
mkdir -p static/uploads

# Install Python dependencies
pip install -r requirements.txt

# Additional build steps here (if any)
echo "Build script completed" 