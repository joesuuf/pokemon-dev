#!/bin/bash
# Simple Vision API test script

echo "Testing Vision API Setup..."
echo ""

# Check if key file exists
if [ ! -f "./gcp-key.json" ]; then
    echo "❌ Error: gcp-key.json not found in current directory"
    echo "   Make sure you're in the directory where you saved the key file"
    exit 1
fi
echo "✓ Key file found: ./gcp-key.json"

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
echo "✓ Environment variable set: GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json"

# Check if package is installed
if [ ! -d "node_modules/@google-cloud/vision" ]; then
    echo ""
    echo "⚠ Package @google-cloud/vision not installed"
    echo "  Installing..."
    npm install @google-cloud/vision
fi

# Test
echo ""
echo "Testing Vision API client initialization..."
node test-vision.js

echo ""
echo "✓ Setup complete! You can now use Vision API."
