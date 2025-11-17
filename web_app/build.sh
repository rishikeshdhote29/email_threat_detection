#!/bin/bash
# Build script for React app deployment

echo "🚀 Starting React app build..."

# Set proper permissions for node_modules
chmod -R +x node_modules/.bin/

# Install dependencies
npm ci --only=production=false

# Build the app with CI=false to ignore warnings
CI=false npm run build

echo "✅ Build completed successfully!"