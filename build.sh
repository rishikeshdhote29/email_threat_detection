#!/bin/bash
# Build script for Render deployment

# Set Python version preference
export PYTHON_VERSION=3.12.7

# Upgrade pip and install build tools first
python -m pip install --upgrade pip==25.3
python -m pip install --upgrade setuptools==75.6.0 wheel==0.44.0

# Clear pip cache to avoid conflicts
python -m pip cache purge

# Install dependencies with no cache and verbose output
python -m pip install --no-cache-dir --verbose -r requirements.txt

echo "✅ Build completed successfully!"