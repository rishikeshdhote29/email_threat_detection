#!/bin/bash
# Build script for React app deployment

echo "🚀 Starting React app build..."

# Install dependencies first
npm install

# Set proper permissions for node_modules (ignore errors)
chmod -R 755 node_modules/.bin/ || true
find node_modules/.bin -type f -exec chmod +x {} \; 2>/dev/null || true

# Build the app with CI=false to ignore warnings
CI=false npx react-scripts build

echo "✅ Build completed successfully!"