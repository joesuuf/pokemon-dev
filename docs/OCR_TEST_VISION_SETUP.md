# Quick Test Commands for Vision API Setup

## Test Vision API Authentication

### Option 1: Simple Node.js Test (Single Line)
```bash
node -e "const {ImageAnnotatorClient} = require('@google-cloud/vision'); const client = new ImageAnnotatorClient(); console.log('Success');"
```

### Option 2: Create Test File
```bash
# Create test file
cat > test-vision.js << 'EOF'
const {ImageAnnotatorClient} = require('@google-cloud/vision');
const client = new ImageAnnotatorClient();
console.log('Vision API client initialized successfully');
EOF

# Run test
node test-vision.js
```

### Option 3: Python Test
```bash
python3 -c "from google.cloud import vision; client = vision.ImageAnnotatorClient(); print('Success')"
```

## Verify Service Account Key

```bash
# Check if key file exists
ls -la ./gcp-key.json

# Verify it's valid JSON
cat ./gcp-key.json | jq '.type'  # Should output: "service_account"

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Verify environment variable is set
echo $GOOGLE_APPLICATION_CREDENTIALS
```

## Full Test Script

Save this as `test-vision-setup.sh`:

```bash
#!/bin/bash
set -e

echo "Testing Vision API Setup..."
echo ""

# Check if key file exists
if [ ! -f "./gcp-key.json" ]; then
    echo "? Error: gcp-key.json not found"
    exit 1
fi
echo "? Key file exists"

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
echo "? Environment variable set"

# Test Node.js (if installed)
if command -v node &> /dev/null; then
    echo ""
    echo "Testing with Node.js..."
    node -e "const {ImageAnnotatorClient} = require('@google-cloud/vision'); const client = new ImageAnnotatorClient(); console.log('? Node.js test successful');" 2>&1 || echo "? Node.js test failed (may need: npm install @google-cloud/vision)"
else
    echo "? Node.js not installed, skipping Node.js test"
fi

# Test Python (if installed)
if command -v python3 &> /dev/null; then
    echo ""
    echo "Testing with Python..."
    python3 -c "from google.cloud import vision; client = vision.ImageAnnotatorClient(); print('? Python test successful')" 2>&1 || echo "? Python test failed (may need: pip install google-cloud-vision)"
else
    echo "? Python3 not installed, skipping Python test"
fi

echo ""
echo "Setup verification complete!"
```

Run it:
```bash
chmod +x test-vision-setup.sh
./test-vision-setup.sh
```
