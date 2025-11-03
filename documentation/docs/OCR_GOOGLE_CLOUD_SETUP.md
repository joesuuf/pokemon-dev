# Google Cloud Platform Setup Guide

## Overview
Complete setup guide for OCR feature using **exclusively Google Cloud Platform services**.

## Prerequisites
- Google Cloud account (free tier available)
- GCP project created
- `gcloud` CLI installed and authenticated

## Step 1: Create GCP Project

```bash
# Create new project
gcloud projects create pokemon-ocr --name="Pokemon OCR"

# Set as active project
gcloud config set project pokemon-ocr

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
echo "Project ID: $PROJECT_ID"
```

## Step 2: Enable Required APIs

```bash
# Enable Vision API
gcloud services enable vision.googleapis.com

# Enable Cloud Run (for serverless backend)
gcloud services enable run.googleapis.com

# Enable Cloud Storage (for image storage, optional)
gcloud services enable storage.googleapis.com

# Enable Secret Manager (for credentials, recommended)
gcloud services enable secretmanager.googleapis.com
```

## Step 3: Create Service Account

```bash
# Create service account for Vision API access
gcloud iam service-accounts create vision-service \
  --display-name="Vision API Service" \
  --description="Service account for OCR Vision API access"

# Get service account email
SA_EMAIL="vision-service@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant Vision API permissions
# Note: Use roles/ml.developer or grant specific API access
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/ml.developer"

# Create and download key for local development
gcloud iam service-accounts keys create ./gcp-key.json \
  --iam-account=${SA_EMAIL}
```

## Step 4: Store Credentials in Secret Manager (Production)

```bash
# Create secret for service account key
gcloud secrets create vision-service-account-key \
  --data-file=./gcp-key.json \
  --replication-policy="automatic"

# Verify secret created
gcloud secrets versions access latest --secret="vision-service-account-key"
```

## Step 5: Set Up Cloud Storage Bucket (Optional)

If you want to store uploaded images:

```bash
# Create bucket
BUCKET_NAME="pokemon-ocr-images-${PROJECT_ID}"
gsutil mb -p ${PROJECT_ID} -l us-central1 gs://${BUCKET_NAME}

# Set bucket permissions
gsutil iam ch serviceAccount:${SA_EMAIL}:roles/storage.objectAdmin \
  gs://${BUCKET_NAME}
```

## Step 6: Configure Local Development

```bash
# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Or add to .env file
echo "GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json" >> .env
```

## Step 7: Deploy to Cloud Run (Optional)

### Option A: Deploy Node.js/Express Backend

```bash
# Build Docker image
docker build -t gcr.io/${PROJECT_ID}/ocr-backend:latest .

# Push to Container Registry
docker push gcr.io/${PROJECT_ID}/ocr-backend:latest

# Deploy to Cloud Run
gcloud run deploy ocr-backend \
  --image gcr.io/${PROJECT_ID}/ocr-backend:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars POKEMON_TCG_API_KEY=your-key \
  --set-secrets GOOGLE_APPLICATION_CREDENTIALS=vision-service-account-key:latest \
  --memory 512Mi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10
```

### Option B: Deploy Python/FastAPI Backend

```bash
# Similar process with Python Dockerfile
docker build -t gcr.io/${PROJECT_ID}/ocr-backend-python:latest -f Dockerfile.python .

docker push gcr.io/${PROJECT_ID}/ocr-backend-python:latest

gcloud run deploy ocr-backend-python \
  --image gcr.io/${PROJECT_ID}/ocr-backend-python:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars POKEMON_TCG_API_KEY=your-key \
  --set-secrets GOOGLE_APPLICATION_CREDENTIALS=vision-service-account-key:latest
```

## Step 8: Configure CORS for Frontend

If deploying to Cloud Run, configure CORS:

```bash
# CORS is configured in backend code
# Cloud Run automatically handles HTTPS
```

## Step 9: Set Up Billing Alerts

```bash
# Create budget alert (optional but recommended)
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Pokemon OCR Budget" \
  --budget-amount=50USD \
  --threshold-rule=percent=90 \
  --threshold-rule=percent=100
```

## Step 10: Test Vision API Access

```bash
# Test Vision API with a sample image
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://vision.googleapis.com/v1/images:annotate \
  -d '{
    "requests": [{
      "image": {
        "source": {
          "imageUri": "https://storage.googleapis.com/example-image.jpg"
        }
      },
      "features": [{
        "type": "TEXT_DETECTION"
      }]
    }]
  }'
```

## Environment Variables Summary

### Local Development
```bash
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json
POKEMON_TCG_API_KEY=your-key
PORT=3001
```

### Cloud Run (Set in deployment)
```bash
GOOGLE_APPLICATION_CREDENTIALS=path/to/secret  # From Secret Manager
POKEMON_TCG_API_KEY=your-key                   # Environment variable
```

## Cost Estimation

### Google Cloud Vision API
- **First 1,000 units/month**: FREE
- **1,001-5,000,000 units/month**: $1.50 per 1,000 units
- **Each OCR request**: ~1 unit

### Cloud Run
- **CPU**: $0.00002400 per vCPU-second
- **Memory**: $0.00000250 per GiB-second
- **Requests**: $0.40 per million requests
- **Free tier**: 2 million requests/month

### Cloud Storage (if used)
- **Storage**: $0.020 per GB/month
- **Operations**: $0.05 per 10,000 operations
- **Free tier**: 5 GB storage/month

### Estimated Monthly Cost
- **Low usage** (1,000 OCR requests/month): **FREE**
- **Medium usage** (10,000 OCR requests/month): **~$13.50**
- **High usage** (100,000 OCR requests/month): **~$148.50**

## Security Best Practices

1. **Never commit credentials**: Add `gcp-key.json` to `.gitignore`
2. **Use Secret Manager**: Store secrets in Google Secret Manager for production
3. **IAM Roles**: Use least privilege principle for service accounts
4. **CORS**: Configure CORS to only allow your frontend domain
5. **HTTPS**: Cloud Run automatically provides HTTPS
6. **Rate Limiting**: Implement rate limiting in backend code

## Troubleshooting

### Issue: "Permission denied" when calling Vision API
```bash
# Check service account permissions
gcloud projects get-iam-policy ${PROJECT_ID} \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:${SA_EMAIL}"
```

### Issue: "API not enabled"
```bash
# Enable Vision API
gcloud services enable vision.googleapis.com

# Verify enabled
gcloud services list --enabled | grep vision
```

### Issue: Billing not enabled
```bash
# Link billing account
gcloud billing projects link ${PROJECT_ID} --billing-account=BILLING_ACCOUNT_ID
```

## Next Steps

1. ? Complete GCP setup
2. ? Create service account and download key
3. ? Test Vision API access
4. ? Set up backend deployment (Cloud Run or local)
5. ? Configure frontend to connect to backend
6. ? Test end-to-end OCR flow

For detailed implementation, see:
- `docs/OCR_CARD_IDENTIFICATION_FEATURE_PLAN.md`
- `docs/OCR_TECHNICAL_IMPLEMENTATION.md`
