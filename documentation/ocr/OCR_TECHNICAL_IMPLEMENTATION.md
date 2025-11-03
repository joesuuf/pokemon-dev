## Google Cloud Platform - Only Integration

This implementation uses **exclusively Google Cloud Platform services**:
- Google Cloud Vision API (OCR)
- Google Cloud Run (Backend API hosting)
- Google Cloud Storage (Optional image storage)
- Google Secret Manager (Credentials)

No Vercel, Supabase, or other third-party services.

### 1. GCP Setup
```bash
# Install GCP CLI (if not already installed)
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Create a new project or use existing
gcloud projects create pokemon-ocr-project --name="Pokemon OCR"

# Enable Vision API
gcloud services enable vision.googleapis.com

# Create service account
gcloud iam service-accounts create vision-api-service \
  --display-name="Vision API Service"

# Grant permissions
gcloud projects add-iam-policy-binding pokemon-ocr-project \
  --member="serviceAccount:vision-api-service@pokemon-ocr-project.iam.gserviceaccount.com" \
  --role="roles/vision.user"

# Create and download key
gcloud iam service-accounts keys create ./gcp-key.json \
  --iam-account=vision-api-service@pokemon-ocr-project.iam.gserviceaccount.com
```

### 2. Install Dependencies
```bash
npm install @google-cloud/vision react-dropzone
npm install --save-dev @types/react-dropzone
```

### 3. Environment Variables

**Local Development (.env):**
```bash
# Google Cloud Vision API
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Pokemon TCG API (existing, read-only)
POKEMON_TCG_API_KEY=your-pokemon-tcg-api-key

# Backend Server (if running locally)
PORT=3001
CORS_ORIGIN=http://localhost:5173
```

**Google Cloud Run (Production):**
- Set environment variables in Cloud Run console
- Use Secret Manager for sensitive credentials
- `GOOGLE_APPLICATION_CREDENTIALS` is automatically handled by Cloud Run

---

## Backend Implementation

### Google Cloud Run Deployment

The backend can be deployed to Google Cloud Run for a fully serverless, Google-only solution:

```bash
# Build Docker image
docker build -t gcr.io/pokemon-ocr/ocr-backend .

# Push to Google Container Registry
docker push gcr.io/pokemon-ocr/ocr-backend

# Deploy to Cloud Run
gcloud run deploy ocr-backend \
  --image gcr.io/pokemon-ocr/ocr-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars POKEMON_TCG_API_KEY=your-key \
  --set-secrets GOOGLE_APPLICATION_CREDENTIALS=vision-service-account-key:latest
```

### Local Development: Express Server

For local development, use Express. For production, deploy to Cloud Run.

### API Endpoint: Express Route `/api/ocr/upload`

```typescript
import express, { Request, Response } from 'express';
import multer from 'multer';
import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';

const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  storage: multer.memoryStorage(),
});

const router = express.Router();

router.post('/upload', upload.single('image'), async (req: Request, res: Response) => {
  if (!req.file) {
    return res.status(400).json({ error: 'No image file provided' });
  }

  // Validate file type
  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!allowedTypes.includes(req.file.mimetype)) {
    return res.status(400).json({
      error: 'Invalid file type',
      allowedTypes,
    });
  }

  try {
    // Convert to base64
    const base64Image = req.file.buffer.toString('base64');
    const dataUrl = `data:${req.file.mimetype};base64,${base64Image}`;

    // Generate unique ID
    const imageId = uuidv4();

    return res.status(200).json({
      success: true,
      imageId,
      previewUrl: dataUrl,
    });
  } catch (error) {
    console.error('[OCR Upload] Error:', error);
    return res.status(500).json({
      error: 'Failed to process image upload',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
});

export default router;
```

### API Endpoint: Express Route `/api/ocr/process`

```typescript
import express, { Request, Response } from 'express';
import { ImageAnnotatorClient } from '@google-cloud/vision';

// Initialize Vision API client
const visionClient = new ImageAnnotatorClient();

interface OCRRegions {
  name: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

interface ProcessRequest {
  imageData: string; // base64 or data URL
  regions?: OCRRegions[];
}

router.post('/process', async (req: Request, res: Response) => {
  try {
    const { imageData, regions }: ProcessRequest = req.body;

    if (!imageData) {
      return res.status(400).json({ error: 'Missing imageData' });
    }

    // Extract base64 from data URL if needed
    let base64Image = imageData;
    if (imageData.startsWith('data:')) {
      base64Image = imageData.split(',')[1];
    }

    const imageBuffer = Buffer.from(base64Image, 'base64');

    // Call GCP Vision API
    const [result] = await visionClient.textDetection({
      image: { content: imageBuffer },
      imageContext: {
        // Specify regions if provided
        ...(regions && regions.length > 0 && {
          cropHintsParams: {
            cropHints: regions.map((region) => ({
              aspectRatios: [region.width / region.height],
            })),
          },
        }),
      },
    });

    const detections = result.textAnnotations || [];
    const fullText = detections[0]?.description || '';

    // Extract text from specific regions
    const textRegions: Record<string, string> = {
      fullText,
    };

    // Parse regions if provided
    if (regions && detections.length > 1) {
      for (const region of regions) {
        // Find text in region (simplified - would need coordinate matching)
        const regionText = extractTextFromRegion(detections, region);
        if (regionText) {
          textRegions[region.name] = regionText;
        }
      }
    }

    // Extract card identifiers from full text
    const cardInfo = parseCardText(fullText);

    return res.status(200).json({
      success: true,
      textRegions,
      cardInfo,
      confidence: cardInfo.confidence,
    });
  } catch (error) {
    console.error('[OCR Process] Error:', error);
    return res.status(500).json({
      error: 'Failed to process OCR',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}

function extractTextFromRegion(
  detections: any[],
  region: OCRRegions
): string | null {
  // Simplified - would need proper coordinate matching
  // In production, match text annotation bounding boxes to region
  return null;
}

function parseCardText(text: string): {
  setCode?: string;
  cardNumber?: string;
  fullCardId?: string;
  confidence: number;
} {
  // Pattern 1: Full card ID (e.g., "swsh4-73")
  const fullIdMatch = text.match(/([a-z]+)(\d+)-(\d+)/i);
  if (fullIdMatch) {
    return {
      setCode: fullIdMatch[1] + fullIdMatch[2],
      cardNumber: fullIdMatch[3],
      fullCardId: fullIdMatch[0],
      confidence: 0.95,
    };
  }

  // Pattern 2: Set abbreviation + number (e.g., "SM 25/236")
  const setNumberMatch = text.match(/([A-Z]{2,4})\s*(\d+)\/(\d+)/i);
  if (setNumberMatch) {
    return {
      setCode: setNumberMatch[1],
      cardNumber: setNumberMatch[2],
      confidence: 0.90,
    };
  }

  // Pattern 3: Set code + number (e.g., "sm1-1")
  const codeNumberMatch = text.match(/([a-z]+\d+)-(\d+)/i);
  if (codeNumberMatch) {
    return {
      setCode: codeNumberMatch[1],
      cardNumber: codeNumberMatch[2],
      fullCardId: codeNumberMatch[0],
      confidence: 0.92,
    };
  }

  return { confidence: 0.0 };
}
```

### API Endpoint: Express Route `/api/ocr/match`

```typescript
import express, { Request, Response } from 'express';
import type { PokemonCard } from '../../src/types/pokemon';

interface OCRResults {
  setCode?: string;
  cardNumber?: string;
  fullCardId?: string;
  setName?: string;
}

interface MatchRequest {
  ocrResults: OCRResults;
}

router.post('/match', async (req: Request, res: Response) => {
  const startTime = Date.now();

  try {
    const { ocrResults }: MatchRequest = req.body;

    if (!ocrResults) {
      return res.status(400).json({ error: 'Missing ocrResults' });
    }

    const apiKey = process.env.POKEMON_TCG_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'API key not configured' });
    }

    const matches: Array<{
      card: PokemonCard;
      confidence: number;
      matchReason: string;
      matchedFields: string[];
    }> = [];

    // Strategy 1: Exact ID match
    if (ocrResults.fullCardId) {
      try {
        const response = await fetch(
          `https://api.pokemontcg.io/v2/cards/${ocrResults.fullCardId}`,
          {
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          matches.push({
            card: data.data,
            confidence: 0.98,
            matchReason: 'exact_id_match',
            matchedFields: ['id'],
          });
        }
      } catch (error) {
        console.error('[Match] Exact ID match failed:', error);
      }
    }

    // Strategy 2: Set code + number match
    if (ocrResults.setCode && ocrResults.cardNumber && matches.length === 0) {
      try {
        const query = `set.id:${ocrResults.setCode.toLowerCase()} AND number:${ocrResults.cardNumber}`;
        const response = await fetch(
          `https://api.pokemontcg.io/v2/cards?q=${encodeURIComponent(query)}&pageSize=5`,
          {
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data.data && data.data.length > 0) {
            const confidence = data.data.length === 1 ? 0.95 : 0.85;
            data.data.forEach((card: PokemonCard) => {
              matches.push({
                card,
                confidence,
                matchReason: 'set_number_match',
                matchedFields: ['set.id', 'number'],
              });
            });
          }
        }
      } catch (error) {
        console.error('[Match] Set+Number match failed:', error);
      }
    }

    // Strategy 3: Set name + number match (fuzzy)
    if (ocrResults.setName && ocrResults.cardNumber && matches.length === 0) {
      try {
        const query = `set.name:"${ocrResults.setName}" AND number:${ocrResults.cardNumber}`;
        const response = await fetch(
          `https://api.pokemontcg.io/v2/cards?q=${encodeURIComponent(query)}&pageSize=5`,
          {
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data.data && data.data.length > 0) {
            const confidence = data.data.length === 1 ? 0.90 : 0.80;
            data.data.forEach((card: PokemonCard) => {
              matches.push({
                card,
                confidence,
                matchReason: 'set_name_match',
                matchedFields: ['set.name', 'number'],
              });
            });
          }
        }
      } catch (error) {
        console.error('[Match] SetName+Number match failed:', error);
      }
    }

    // Sort by confidence (highest first)
    matches.sort((a, b) => b.confidence - a.confidence);

    // Filter to 95%+ confidence matches
    const highConfidenceMatches = matches.filter((m) => m.confidence >= 0.95);

    const processingTime = Date.now() - startTime;

    return res.status(200).json({
      success: true,
      matches: highConfidenceMatches.length > 0 ? highConfidenceMatches : matches,
      allMatches: matches,
      processingTime,
      hasHighConfidence: highConfidenceMatches.length > 0,
    });
  } catch (error) {
    console.error('[OCR Match] Error:', error);
    return res.status(500).json({
      error: 'Failed to match card',
      message: error instanceof Error ? error.message : 'Unknown error',
    });
  }
}
```

---

## Frontend Implementation

### Service: `src/services/ocrService.ts`

```typescript
import type { PokemonCard } from '../types/pokemon';

export interface OCRUploadResponse {
  success: boolean;
  imageId: string;
  previewUrl: string;
}

export interface OCRProcessResponse {
  success: boolean;
  textRegions: {
    bottomLeft?: string;
    bottomRight?: string;
    fullText: string;
  };
  cardInfo: {
    setCode?: string;
    cardNumber?: string;
    fullCardId?: string;
    confidence: number;
  };
  confidence: number;
}

export interface OCRMatchResponse {
  success: boolean;
  matches: Array<{
    card: PokemonCard;
    confidence: number;
    matchReason: string;
    matchedFields: string[];
  }>;
  allMatches: Array<{
    card: PokemonCard;
    confidence: number;
    matchReason: string;
    matchedFields: string[];
  }>;
  processingTime: number;
  hasHighConfidence: boolean;
}

export async function uploadImage(file: File): Promise<OCRUploadResponse> {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch('/api/ocr/upload', {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to upload image');
  }

  return response.json();
}

export async function processOCR(imageData: string): Promise<OCRProcessResponse> {
  const response = await fetch('/api/ocr/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      imageData,
      regions: [
        { name: 'bottomLeft', x: 0.0, y: 0.8, width: 0.2, height: 0.2 },
        { name: 'bottomRight', x: 0.8, y: 0.8, width: 0.2, height: 0.2 },
      ],
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to process OCR');
  }

  return response.json();
}

export async function matchCard(ocrResults: {
  setCode?: string;
  cardNumber?: string;
  fullCardId?: string;
  setName?: string;
}): Promise<OCRMatchResponse> {
  const response = await fetch('/api/ocr/match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ocrResults }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to match card');
  }

  return response.json();
}
```

### Component: `src/components/ImageUpload.tsx`

```typescript
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  maxSize?: number;
  acceptedFormats?: string[];
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageSelect,
  maxSize = 5 * 1024 * 1024, // 5MB
  acceptedFormats = ['image/jpeg', 'image/png', 'image/webp'],
}) => {
  const [preview, setPreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      // Validate size
      if (file.size > maxSize) {
        setError(`File too large. Maximum size: ${maxSize / 1024 / 1024}MB`);
        return;
      }

      // Create preview
      const reader = new FileReader();
      reader.onload = () => {
        setPreview(reader.result as string);
        setError(null);
        onImageSelect(file);
      };
      reader.readAsDataURL(file);
    },
    [maxSize, onImageSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: acceptedFormats.reduce((acc, format) => {
      acc[format] = [];
      return acc;
    }, {} as Record<string, string[]>),
    maxFiles: 1,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors
          ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
          ${error ? 'border-red-500 bg-red-50' : ''}
        `}
      >
        <input {...getInputProps()} />
        {preview ? (
          <div className="space-y-4">
            <img
              src={preview}
              alt="Preview"
              className="max-w-full max-h-64 mx-auto rounded"
            />
            <p className="text-sm text-gray-600">
              Click or drag to replace image
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-lg font-medium">
              {isDragActive
                ? 'Drop the image here'
                : 'Drag & drop a card image, or click to select'}
            </p>
            <p className="text-sm text-gray-500">
              Supports: JPEG, PNG, WebP (max {maxSize / 1024 / 1024}MB)
            </p>
          </div>
        )}
      </div>
      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};
```

### Component: `src/components/OCRProcessing.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import { uploadImage, processOCR, matchCard, type OCRMatchResponse } from '../services/ocrService';
import type { PokemonCard } from '../types/pokemon';

interface OCRProcessingProps {
  imageFile: File;
  onComplete: (results: OCRMatchResponse) => void;
  onError: (error: Error) => void;
}

export const OCRProcessing: React.FC<OCRProcessingProps> = ({
  imageFile,
  onComplete,
  onError,
}) => {
  const [step, setStep] = useState<'upload' | 'ocr' | 'match' | 'complete'>('upload');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const process = async () => {
      try {
        // Step 1: Upload
        setStep('upload');
        setProgress(25);
        const uploadResult = await uploadImage(imageFile);

        // Step 2: OCR
        setStep('ocr');
        setProgress(50);
        const ocrResult = await processOCR(uploadResult.previewUrl);

        // Step 3: Match
        setStep('match');
        setProgress(75);
        const matchResult = await matchCard(ocrResult.cardInfo);

        // Complete
        setStep('complete');
        setProgress(100);
        onComplete(matchResult);
      } catch (error) {
        onError(error instanceof Error ? error : new Error('Unknown error'));
      }
    };

    process();
  }, [imageFile, onComplete, onError]);

  const stepLabels = {
    upload: 'Uploading image...',
    ocr: 'Extracting text...',
    match: 'Matching card...',
    complete: 'Complete!',
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">{stepLabels[step]}</span>
        <span className="text-sm text-gray-500">{progress}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  );
};
```

### Component: `src/components/CardMatchResult.tsx`

```typescript
import React from 'react';
import type { PokemonCard } from '../types/pokemon';

interface CardMatchResultProps {
  match: {
    card: PokemonCard;
    confidence: number;
    matchReason: string;
    matchedFields: string[];
  };
  onSelect: (card: PokemonCard) => void;
}

export const CardMatchResult: React.FC<CardMatchResultProps> = ({
  match,
  onSelect,
}) => {
  const confidenceColor =
    match.confidence >= 0.95
      ? 'text-green-600 bg-green-50'
      : match.confidence >= 0.85
      ? 'text-yellow-600 bg-yellow-50'
      : 'text-red-600 bg-red-50';

  return (
    <div className="border rounded-lg p-4 hover:shadow-lg transition-shadow">
      <div className="flex items-start gap-4">
        <img
          src={match.card.images.small}
          alt={match.card.name}
          className="w-32 h-44 object-contain rounded"
          loading="lazy"
        />
        <div className="flex-1 space-y-2">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold">{match.card.name}</h3>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${confidenceColor}`}
            >
              {(match.confidence * 100).toFixed(0)}% confidence
            </span>
          </div>
          <p className="text-sm text-gray-600">
            {match.card.set.name} ? #{match.card.number}
          </p>
          <p className="text-xs text-gray-500">
            Matched by: {match.matchReason.replace('_', ' ')}
          </p>
          <button
            onClick={() => onSelect(match.card)}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
          >
            View Details
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## Integration Example

### Add to `App.tsx` or new route

```typescript
import { useState } from 'react';
import { ImageUpload } from './components/ImageUpload';
import { OCRProcessing } from './components/OCRProcessing';
import { CardMatchResult } from './components/CardMatchResult';
import type { OCRMatchResponse } from './services/ocrService';

export const OCRSearch = () => {
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState<OCRMatchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelect = (file: File) => {
    setImageFile(file);
    setProcessing(true);
    setResults(null);
    setError(null);
  };

  const handleComplete = (matchResults: OCRMatchResponse) => {
    setProcessing(false);
    setResults(matchResults);
  };

  const handleError = (err: Error) => {
    setProcessing(false);
    setError(err.message);
  };

  return (
    <div className="container mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold">OCR Card Search</h1>
      
      <ImageUpload onImageSelect={handleImageSelect} />

      {processing && imageFile && (
        <OCRProcessing
          imageFile={imageFile}
          onComplete={handleComplete}
          onError={handleError}
        />
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700">
          {error}
        </div>
      )}

      {results && (
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">
            Found {results.matches.length} match(es)
          </h2>
          {results.matches.map((match, index) => (
            <CardMatchResult
              key={index}
              match={match}
              onSelect={(card) => {
                // Navigate to card details or show modal
                console.log('Selected card:', card);
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
};
```

---

## Testing

### Test OCR Text Parsing

```typescript
import { describe, it, expect } from 'vitest';
import { parseCardText } from '../api/ocr/process';

describe('parseCardText', () => {
  it('should parse full card ID format', () => {
    const result = parseCardText('swsh4-73');
    expect(result.fullCardId).toBe('swsh4-73');
    expect(result.confidence).toBeGreaterThan(0.9);
  });

  it('should parse set abbreviation format', () => {
    const result = parseCardText('SM 25/236');
    expect(result.setCode).toBe('SM');
    expect(result.cardNumber).toBe('25');
  });

  it('should return low confidence for invalid text', () => {
    const result = parseCardText('random text');
    expect(result.confidence).toBe(0.0);
  });
});
```

---

## Next Steps

1. **Review and approve plan**
2. **Set up GCP credentials**
3. **Install dependencies**
4. **Implement backend endpoints**
5. **Create frontend components**
6. **Test end-to-end**
7. **Deploy to production**

For full details, see: `docs/OCR_CARD_IDENTIFICATION_FEATURE_PLAN.md`
