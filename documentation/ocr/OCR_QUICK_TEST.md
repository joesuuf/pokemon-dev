# Quick Vision API Test - Copy and Paste This

Run these commands one at a time:

```bash
# 1. Navigate to where your gcp-key.json file is
cd ~
# (or wherever you saved gcp-key.json)

# 2. Set the credentials environment variable
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# 3. Install the package (if not already installed)
npm install @google-cloud/vision

# 4. Run this inline test (copy the entire line):
node -e "const vision=require('@google-cloud/vision');const client=new vision.ImageAnnotatorClient();console.log('Success: Vision API client initialized')"

# Or create a simple test file:
cat > test-vision.js << 'TESTEOF'
const vision = require('@google-cloud/vision');
const client = new vision.ImageAnnotatorClient();
console.log('Success: Vision API client initialized');
TESTEOF

# Then run:
node test-vision.js
```

## Alternative: Python Test (if Node.js doesn't work)

```bash
# Install Python package
pip3 install google-cloud-vision

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Test
python3 -c "from google.cloud import vision; client = vision.ImageAnnotatorClient(); print('Success')"
```
