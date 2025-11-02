# Fix for Vision API IAM Role Error

## Issue
The role `roles/vision.user` doesn't exist. Vision API uses different permission model.

## Solution Options

### Option 1: Use roles/ml.developer (Recommended)
This role provides access to Machine Learning APIs including Vision API:

```bash
gcloud projects add-iam-policy-binding chk-poke-ocr \
  --member="serviceAccount:chk-poke-vision-service@chk-poke-ocr.iam.gserviceaccount.com" \
  --role="roles/ml.developer"
```

### Option 2: Minimal Role - No Project-Level Role Needed
For Vision API, you might not need a project-level IAM role. The service account key file provides authentication, and enabling the API grants access. Try this first:

```bash
# Just enable the API (already done)
gcloud services enable vision.googleapis.com

# Test if it works without the role binding
# If authentication works, you're good to go!
```

### Option 3: Use Service Account User Role
If you need explicit permissions, use a more generic role:

```bash
gcloud projects add-iam-policy-binding chk-poke-ocr \
  --member="serviceAccount:chk-poke-vision-service@chk-poke-ocr.iam.gserviceaccount.com" \
  --role="roles/serviceusage.serviceUsageConsumer"
```

### Option 4: Use Custom Role (Most Restrictive)
Create a custom role with only Vision API permissions:

```bash
# Create custom role
gcloud iam roles create visionApiUser \
  --project=chk-poke-ocr \
  --title="Vision API User" \
  --description="Can use Vision API" \
  --permissions=ml.images.annotate,ml.images.predict

# Grant custom role
gcloud projects add-iam-policy-binding chk-poke-ocr \
  --member="serviceAccount:chk-poke-vision-service@chk-poke-ocr.iam.gserviceaccount.com" \
  --role="projects/chk-poke-ocr/roles/visionApiUser"
```

## Recommended Fix for Your Project

Since you already have the service account created and key downloaded, try Option 1 first:

```bash
gcloud projects add-iam-policy-binding chk-poke-ocr \
  --member="serviceAccount:chk-poke-vision-service@chk-poke-ocr.iam.gserviceaccount.com" \
  --role="roles/ml.developer"
```

If that doesn't work or you want minimal permissions, try Option 2 (no role binding) - Vision API might work with just authentication via the service account key.

## Verify Setup

Test if Vision API works:

```bash
# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Test with a simple Node.js script or Python
node -e "const {ImageAnnotatorClient} = require('@google-cloud/vision'); const client = new ImageAnnotatorClient(); console.log('Vision API client initialized successfully');"
```

Or test with Python:

```python
from google.cloud import vision
client = vision.ImageAnnotatorClient()
print("Vision API client initialized successfully")
```

## Note
The service account key file (`gcp-key.json`) you created provides authentication. If the API is enabled and you're authenticated, Vision API calls should work even without a project-level IAM role binding.
