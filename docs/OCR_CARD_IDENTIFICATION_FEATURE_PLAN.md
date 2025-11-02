# OCR Card Identification Feature Plan

## Overview
Add **Google Cloud Platform (GCP) only** integration to identify Pokemon cards from uploaded images using OCR on typical card regions (corners, etc.) and match them to official cards with 95% confidence.

**Google Services Used:**
- Google Cloud Vision API (OCR)
- Google Cloud Storage (optional, for image storage)
- Google Cloud Functions or Cloud Run (optional, for serverless backend)

## Feature Goals
- **Input**: User uploads an image of a Pokemon card
- **Process**: Extract text from card regions using GCP Vision API OCR
- **Output**: Match card to official Pokemon TCG API card with 95%+ confidence
- **UI**: Integrate into existing React frontend with image upload capability

---

## 1. Architecture Overview

### Components
```
Frontend (React/TypeScript)
  ??? ImageUpload Component
  ??? OCR Processing UI
  ??? CardMatch Results Display

Backend API (Vercel Serverless)
  ??? /api/ocr/upload - Image upload endpoint
  ??? /api/ocr/process - OCR processing endpoint
  ??? /api/ocr/match - Card matching endpoint

GCP Services
  ??? Cloud Vision API (OCR)
  ??? Cloud Storage (optional, for image storage)

External API
  ??? Pokemon TCG API v2 (existing integration)
```

### Data Flow
```
1. User uploads image ? Frontend
2. Frontend ? POST /api/ocr/upload (image as base64/form-data)
3. Backend ? GCP Vision API (OCR with region hints)
4. Backend ? Parse OCR results (extract IDs from regions)
5. Backend ? Pokemon TCG API (search by extracted identifiers)
6. Backend ? Confidence scoring algorithm
7. Backend ? Return matched card(s) with confidence scores
8. Frontend ? Display results
```

---

## 2. Pokemon Card ID Locations

### Typical Card Regions (Priority Order)

#### Region 1: Bottom-Left Corner (Highest Priority)
- **Format**: Set symbol + number (e.g., "SM 25/236", "SWSH 073/202")
- **Example**: "SM25" or "SM 25/236"
- **Contains**: Set abbreviation + card number

#### Region 2: Bottom-Right Corner
- **Format**: Set code + number (e.g., "sm1-1", "swsh4-73")
- **Example**: "swsh4-73"
- **Contains**: Full card ID format

#### Region 3: Card ID Field (if visible)
- **Format**: `{set-id}-{number}` (e.g., "sm1-1", "swsh4-73")
- **Example**: "swsh4-73"
- **Contains**: Official API card ID

#### Region 4: Set Name Region
- **Format**: Set name text (e.g., "Sword & Shield?Battle Styles")
- **Can be used for**: Fuzzy matching if numbers fail

### OCR Region Coordinates (Normalized 0-1)
- **Bottom-Left**: `x: 0.0-0.2, y: 0.8-1.0`
- **Bottom-Right**: `x: 0.8-1.0, y: 0.8-1.0`
- **Set Name**: `x: 0.0-0.5, y: 0.1-0.2`

---

## 3. Technical Implementation

### 3.1 GCP Vision API Setup

#### Required Google Cloud Services
- **Cloud Vision API** (OCR) - Primary service
- **Cloud Storage** (optional, for temporary image storage)
- **Cloud Functions** or **Cloud Run** (optional, for serverless backend deployment)

#### API Features to Use
- **TEXT_DETECTION**: Detect text in image
- **DOCUMENT_TEXT_DETECTION**: More accurate OCR (preferred)
- **Region Hints**: Specify regions where IDs are expected

#### Authentication
- Service Account JSON key file
- Environment variable: `GOOGLE_APPLICATION_CREDENTIALS` (points to service account JSON)
- For production: Store credentials securely (environment variable or secure config)

### 3.2 Backend API Endpoints

#### `/api/ocr/upload`
```typescript
POST /api/ocr/upload
Content-Type: multipart/form-data

Request:
  - image: File (image/jpeg, image/png, image/webp)
  - maxSize: 5MB

Response:
{
  "success": true,
  "imageId": "uuid",
  "previewUrl": "data:image/..."
}
```

#### `/api/ocr/process`
```typescript
POST /api/ocr/process
Content-Type: application/json

Request:
{
  "imageData": "base64_string" | "imageId",
  "regions": [
    { "name": "bottomLeft", "x": 0.0, "y": 0.8, "width": 0.2, "height": 0.2 },
    { "name": "bottomRight", "x": 0.8, "y": 0.8, "width": 0.2, "height": 0.2 }
  ]
}

Response:
{
  "success": true,
  "textRegions": {
    "bottomLeft": "SM 25/236",
    "bottomRight": "swsh4-73",
    "fullText": "..."
  },
  "confidence": 0.95
}
```

#### `/api/ocr/match`
```typescript
POST /api/ocr/match
Content-Type: application/json

Request:
{
  "ocrResults": {
    "setCode": "swsh4",
    "cardNumber": "73",
    "setName": "Sword & Shield?Battle Styles",
    "fullCardId": "swsh4-73"
  }
}

Response:
{
  "success": true,
  "matches": [
    {
      "card": PokemonCard,
      "confidence": 0.98,
      "matchReason": "exact_id_match",
      "matchedFields": ["id", "set.id", "number"]
    }
  ],
  "processingTime": 234
}
```

### 3.3 OCR Text Extraction Logic

#### Step 1: GCP Vision API Call
```typescript
import { ImageAnnotatorClient } from '@google-cloud/vision';

const client = new ImageAnnotatorClient();
const [result] = await client.textDetection({
  image: { content: imageBuffer },
  imageContext: {
    // Hint regions where IDs are located
    cropHintsParams: {
      cropHints: [
        { aspectRatios: [0.2, 0.2] }, // bottom-left
        { aspectRatios: [0.2, 0.2] }  // bottom-right
      ]
    }
  }
});
```

#### Step 2: Text Parsing
```typescript
interface ParsedCardInfo {
  setCode?: string;
  cardNumber?: string;
  fullCardId?: string;
  setName?: string;
  confidence: number;
}

function parseOCRText(text: string): ParsedCardInfo {
  // Pattern 1: Full card ID (e.g., "swsh4-73")
  const fullIdMatch = text.match(/([a-z]+)(\d+)-(\d+)/i);
  if (fullIdMatch) {
    return {
      setCode: fullIdMatch[1] + fullIdMatch[2],
      cardNumber: fullIdMatch[3],
      fullCardId: fullIdMatch[0],
      confidence: 0.95
    };
  }

  // Pattern 2: Set abbreviation + number (e.g., "SM 25/236")
  const setNumberMatch = text.match(/([A-Z]{2,4})\s*(\d+)\/(\d+)/i);
  if (setNumberMatch) {
    return {
      setCode: setNumberMatch[1],
      cardNumber: setNumberMatch[2],
      confidence: 0.90
    };
  }

  // Pattern 3: Set code + number (e.g., "sm1-1")
  const codeNumberMatch = text.match(/([a-z]+\d+)-(\d+)/i);
  if (codeNumberMatch) {
    return {
      setCode: codeNumberMatch[1],
      cardNumber: codeNumberMatch[2],
      fullCardId: codeNumberMatch[0],
      confidence: 0.92
    };
  }

  return { confidence: 0.0 };
}
```

### 3.4 Card Matching Logic

#### Strategy 1: Exact ID Match (Highest Confidence)
```typescript
// If we have full card ID: "swsh4-73"
const exactMatch = await fetch(
  `https://api.pokemontcg.io/v2/cards/${fullCardId}`,
  { headers: { 'X-Api-Key': API_KEY } }
);
// Confidence: 0.98
```

#### Strategy 2: Set Code + Number Match
```typescript
// Query: set.id:swsh4 AND number:73
const query = `set.id:${setCode} AND number:${cardNumber}`;
const results = await searchCards({ q: query });
// Confidence: 0.95 if single match, 0.85 if multiple matches
```

#### Strategy 3: Set Name + Number Match
```typescript
// Query: set.name:"Sword & Shield?Battle Styles" AND number:73
const query = `set.name:"${setName}" AND number:${cardNumber}`;
// Confidence: 0.90 if single match
```

#### Strategy 4: Fuzzy Matching (Lower Confidence)
```typescript
// If OCR confidence is low, try fuzzy matching
// Use set name similarity + card number
// Confidence: 0.75-0.85
```

### 3.5 Confidence Scoring Algorithm

```typescript
interface MatchConfidence {
  score: number; // 0.0 - 1.0
  reasons: string[];
  warnings?: string[];
}

function calculateConfidence(
  ocrResult: ParsedCardInfo,
  apiMatch: PokemonCard,
  matchStrategy: string
): MatchConfidence {
  let score = 0.0;
  const reasons: string[] = [];
  const warnings: string[] = [];

  // Base confidence from OCR quality
  score += ocrResult.confidence * 0.3;

  // Strategy-based confidence
  if (matchStrategy === 'exact_id_match') {
    score += 0.5;
    reasons.push('Exact card ID match');
  } else if (matchStrategy === 'set_number_match') {
    score += 0.4;
    reasons.push('Set ID and card number match');
  } else if (matchStrategy === 'set_name_match') {
    score += 0.35;
    reasons.push('Set name and card number match');
  }

  // Additional validation
  if (ocrResult.setCode && apiMatch.set.id.includes(ocrResult.setCode.toLowerCase())) {
    score += 0.1;
    reasons.push('Set code validated');
  }

  if (ocrResult.cardNumber && apiMatch.number === ocrResult.cardNumber) {
    score += 0.1;
    reasons.push('Card number validated');
  }

  // Penalties
  if (score < 0.95) {
    warnings.push('Confidence below 95% threshold');
  }

  return {
    score: Math.min(score, 1.0),
    reasons,
    warnings: warnings.length > 0 ? warnings : undefined
  };
}
```

---

## 4. Frontend Implementation

### 4.1 Components

#### `ImageUpload.tsx`
```typescript
interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  maxSize?: number; // bytes, default 5MB
  acceptedFormats?: string[]; // ['image/jpeg', 'image/png']
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onImageSelect,
  maxSize = 5 * 1024 * 1024,
  acceptedFormats = ['image/jpeg', 'image/png', 'image/webp']
}) => {
  // Drag & drop + file input
  // Image preview
  // Size validation
};
```

#### `OCRProcessing.tsx`
```typescript
interface OCRProcessingProps {
  imageFile: File;
  onComplete: (results: OCRMatchResult) => void;
  onError: (error: Error) => void;
}

export const OCRProcessing: React.FC<OCRProcessingProps> = ({
  imageFile,
  onComplete,
  onError
}) => {
  // Show loading spinner
  // Display progress
  // Call OCR API
  // Show results
};
```

#### `CardMatchResult.tsx`
```typescript
interface CardMatchResultProps {
  match: {
    card: PokemonCard;
    confidence: number;
    matchReason: string;
  };
  onSelect: (card: PokemonCard) => void;
}

export const CardMatchResult: React.FC<CardMatchResultProps> = ({
  match,
  onSelect
}) => {
  // Display matched card
  // Show confidence score
  // Show match reason
  // Link to card details
};
```

### 4.2 API Service

#### `ocrService.ts`
```typescript
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
  processingTime: number;
}

export async function uploadImage(file: File): Promise<OCRUploadResponse> {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch('/api/ocr/upload', {
    method: 'POST',
    body: formData
  });

  return response.json();
}

export async function processOCR(imageData: string): Promise<OCRProcessResponse> {
  const response = await fetch('/api/ocr/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ imageData })
  });

  return response.json();
}

export async function matchCard(ocrResults: ParsedCardInfo): Promise<OCRMatchResponse> {
  const response = await fetch('/api/ocr/match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ocrResults })
  });

  return response.json();
}
---

## 5. Backend Options

### Option A: Node.js/Express (TypeScript) - Recommended for Frontend Integration

**Pros:**
- Same language as frontend (TypeScript)
- Easy integration with existing React app
- Large ecosystem and community support
- Can share types between frontend/backend

**Setup:**
```bash
# Create backend directory
mkdir backend
cd backend
npm init -y

# Install dependencies
npm install express cors multer @google-cloud/vision dotenv axios
npm install --save-dev @types/express @types/cors @types/multer @types/node typescript ts-node nodemon
```

**Structure:**
```
backend/
??? src/
?   ??? routes/
?   ?   ??? ocr.ts
?   ?   ??? index.ts
?   ??? services/
?   ?   ??? vision.ts
?   ?   ??? cardMatcher.ts
?   ??? utils/
?   ?   ??? textParser.ts
?   ??? server.ts
?   ??? types.ts
??? package.json
??? tsconfig.json
??? .env
```

### Option B: Python/FastAPI - Aligns with Existing Python Agents

**Pros:**
- Consistent with existing Python agent infrastructure
- Excellent GCP Vision API support
- FastAPI provides automatic API documentation (Swagger UI)
- Easy to integrate with existing Python tools

**Setup:**
```bash
# Create backend directory
mkdir backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn python-multipart google-cloud-vision httpx python-dotenv pydantic
```

**Structure:**
```
backend/
??? app/
?   ??? routes/
?   ?   ??? ocr.py
?   ?   ??? __init__.py
?   ??? services/
?   ?   ??? vision.py
?   ?   ??? card_matcher.py
?   ??? utils/
?   ?   ??? text_parser.py
?   ??? main.py
?   ??? types.py
??? requirements.txt
??? .env
```

### Recommendation

**Choose Node.js/Express if:**
- You want to share TypeScript types between frontend/backend
- You prefer keeping everything in one language stack
- You want simpler deployment setup

**Choose Python/FastAPI if:**
- You want consistency with existing Python agents
- You prefer Python's ecosystem for ML/AI tasks
- You want automatic API documentation (FastAPI provides Swagger UI)

---

## 6. Dependencies

### Backend Dependencies

#### Node.js/Express Option
```json
{
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "multer": "^1.4.5-lts.1",
    "@google-cloud/vision": "^4.0.0",
    "dotenv": "^16.3.1",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "@types/multer": "^1.4.11",
    "@types/node": "^20.10.0",
    "typescript": "^5.2.2",
    "ts-node": "^10.9.1",
    "nodemon": "^3.0.2"
  }
}
```

#### Python/FastAPI Option
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
google-cloud-vision==3.4.5
httpx==0.25.1
python-dotenv==1.0.0
pydantic==2.5.0
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "react-dropzone": "^14.2.3",
    "@types/react-dropzone": "^5.1.3"
  }
}
```

---

## 7. Backend Deployment Options

### Self-Hosted Options

#### Option 1: Local Development Server
- Run backend on `localhost:3001` (or chosen port)
- Frontend connects via `http://localhost:3001/api/ocr/*`
- Use for development/testing

#### Option 2: Docker Container
- Package backend in Docker container
- Deploy to any Docker-compatible host
- Easy to scale and manage

#### Option 3: Google Cloud Run (Recommended)
- Serverless container platform
- Auto-scaling
- Pay per use
- Integrated with GCP services
- Same GCP project as Vision API

#### Option 4: Google Cloud Functions
- Fully serverless
- Automatic scaling
- Event-driven
- Integrated with GCP services

#### Option 5: Google Compute Engine (VM)
- Full control over environment
- Can use same GCP project as Vision API
- Custom configurations

### Google Cloud Deployment Considerations
- **CORS**: Configure CORS in Cloud Run/Functions to allow frontend domain
- **Environment Variables**: Use Google Secret Manager for credentials
- **Authentication**: Use GCP Service Accounts for Vision API access
- **HTTPS**: Automatically provided by Cloud Run/Functions
- **IAM**: Configure proper IAM roles for Vision API access
- **Billing**: Monitor Vision API usage in GCP Console

---

## Google Cloud Platform Architecture

### Recommended Architecture: Cloud Run + Vision API

```
Frontend (React/TypeScript)
  ? HTTPS
Google Cloud Run (Backend API)
  ??? POST /api/ocr/upload
  ??? POST /api/ocr/process
  ??? POST /api/ocr/match
  ?
Google Cloud Vision API (OCR)
  ?
Google Cloud Run (Card Matching Logic)
  ?
Pokemon TCG API v2 (External, read-only)
```

### Benefits of Google-Only Stack
- **Unified billing**: All costs in one GCP account
- **Integrated security**: IAM roles work across services
- **Easy deployment**: Cloud Run uses same Docker containers
- **Monitoring**: All logs/metrics in Google Cloud Console
- **Cost optimization**: First 1,000 Vision API requests/month free

---

## 8. Environment Variables

### Required
```bash
# GCP Vision API
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json  # Path to GCP service account JSON

# Pokemon TCG API (existing)
POKEMON_TCG_API_KEY=your-pokemon-tcg-api-key

# Backend Server (if using Node.js/Express)
PORT=3001  # Backend API port
CORS_ORIGIN=http://localhost:5173  # Frontend URL for CORS
```

### Google Cloud Setup

#### 1. Create GCP Project
```bash
gcloud projects create pokemon-ocr --name="Pokemon OCR"
gcloud config set project pokemon-ocr
```

#### 2. Enable Required APIs
```bash
# Enable Vision API
gcloud services enable vision.googleapis.com

# Enable Cloud Run (if using)
gcloud services enable run.googleapis.com

# Enable Cloud Storage (if using)
gcloud services enable storage.googleapis.com
```

#### 3. Create Service Account
```bash
# Create service account for Vision API
gcloud iam service-accounts create vision-service \
  --display-name="Vision API Service"

# Grant Vision API permissions
gcloud projects add-iam-policy-binding pokemon-ocr \
  --member="serviceAccount:vision-service@pokemon-ocr.iam.gserviceaccount.com" \
  --role="roles/vision.user"

# Create and download key
gcloud iam service-accounts keys create ./gcp-key.json \
  --iam-account=vision-service@pokemon-ocr.iam.gserviceaccount.com
```

#### 4. Store Credentials in Secret Manager (Production)
```bash
# Store service account key in Secret Manager
gcloud secrets create vision-service-account-key \
  --data-file=./gcp-key.json
```

---

---

## 9. Error Handling

### OCR Errors
- **Image too large**: Return 400 with max size message
- **Unsupported format**: Return 400 with accepted formats
- **GCP API error**: Return 500 with retry suggestion
- **No text detected**: Return 404 with "No card text found" message

### Matching Errors
- **No matches found**: Return 404 with suggestions
- **Multiple matches**: Return 200 with all matches sorted by confidence
- **Low confidence**: Return 200 with warning flag

---

## 10. Testing Strategy

### Unit Tests
- Text parsing functions
- Confidence scoring algorithm
- Region coordinate calculations

### Integration Tests
- GCP Vision API calls (mock)
- Pokemon TCG API matching
- End-to-end OCR ? match flow

### E2E Tests
- Upload image ? OCR ? Match ? Display results

### Test Cases
1. **Perfect card photo**: Bottom-left corner clearly visible
2. **Cropped card**: Only part of card visible
3. **Multiple cards**: Handle edge case
4. **Poor quality**: Low resolution image
5. **Different sets**: Test various set formats
6. **Vintage cards**: Older card formats

---

## 11. Performance Considerations

### Optimization
- **Image compression**: Resize before sending to GCP (max 2048px)
- **Caching**: Cache OCR results for same image hash
- **Batch processing**: If multiple cards, process in parallel
- **Rate limiting**: Limit OCR requests per user

### Expected Performance
- **OCR processing**: 1-3 seconds
- **Card matching**: 0.5-1 second
- **Total**: 2-4 seconds per card

---

## 12. Security Considerations

### Image Upload Security
- **File type validation**: Only allow image formats
- **Size limits**: Max 5MB per image
- **Malware scanning**: Consider scanning uploaded files
- **Rate limiting**: Prevent abuse

### API Security
- **Authentication**: Optional user authentication for OCR
- **API key protection**: Never expose GCP keys in frontend
- **CORS**: Configure CORS for API endpoints

---

## 13. Implementation Phases

### Phase 1: Backend OCR API (Week 1)
- [ ] Choose backend option (Node.js/Express OR Python/FastAPI)
- [ ] Set up backend server structure
- [ ] Set up GCP Vision API credentials
- [ ] Create `POST /api/ocr/upload` endpoint
- [ ] Create `POST /api/ocr/process` endpoint
- [ ] Implement OCR text extraction
- [ ] Implement text parsing logic
- [ ] Write unit tests
- [ ] Configure CORS for frontend access

### Phase 2: Card Matching (Week 1-2)
- [ ] Create `/api/ocr/match` endpoint
- [ ] Implement matching strategies
- [ ] Implement confidence scoring
- [ ] Integrate with Pokemon TCG API
- [ ] Write integration tests

### Phase 3: Frontend UI (Week 2)
- [ ] Create `ImageUpload` component
- [ ] Create `OCRProcessing` component
- [ ] Create `CardMatchResult` component
- [ ] Integrate OCR service
- [ ] Add error handling UI
- [ ] Write component tests

### Phase 4: Integration & Polish (Week 2-3)
- [ ] End-to-end testing
- [ ] Performance optimization
- [ ] Error handling refinement
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Deploy to production

---

## 14. Future Enhancements

### Advanced Features
- **Batch upload**: Process multiple cards at once
- **Card condition detection**: Detect card condition from image
- **Price estimation**: Show estimated value based on condition
- **Collection tracking**: Save OCR'd cards to collection
- **Mobile app**: Native mobile app with camera integration

### AI Improvements
- **Card recognition**: Use ML to detect card orientation/quality
- **Better OCR**: Fine-tune OCR for Pokemon cards specifically
- **Visual matching**: Compare card images directly (not just OCR)

---

## 15. Success Metrics

### Technical Metrics
- **OCR accuracy**: >95% correct text extraction
- **Match confidence**: >95% for clear images
- **Processing time**: <5 seconds per card
- **Error rate**: <5% failure rate

### User Metrics
- **Upload success rate**: >90%
- **Match success rate**: >85% for clear images
- **User satisfaction**: Positive feedback on feature

---

## 16. Documentation

### User Documentation
- How to upload card images
- Best practices for photo quality
- Understanding confidence scores
- Troubleshooting common issues

### Developer Documentation
- API endpoint documentation
- OCR region specifications
- Matching algorithm details
- Contributing guidelines

---

## 17. Cost Estimation

### GCP Vision API Costs
- **First 1,000 units/month**: Free
- **1,001-5,000,000 units/month**: $1.50 per 1,000 units
- **Estimate**: ~$0.0015 per OCR request

### Expected Usage
- **Conservative**: 1,000 requests/month = Free
- **Moderate**: 10,000 requests/month = ~$13.50/month
- **High**: 100,000 requests/month = ~$148.50/month

---

## Appendix: Example API Responses

### OCR Process Response
```json
{
  "success": true,
  "textRegions": {
    "bottomLeft": "SM 25/236",
    "bottomRight": "swsh4-73",
    "fullText": "Charizard\nHP 150\n[Fire] [Fire] [Fire] Inferno Overdrive 300\nSM 25/236"
  },
  "confidence": 0.96
}
```

### Match Response
```json
{
  "success": true,
  "matches": [
    {
      "card": {
        "id": "swsh4-73",
        "name": "Charizard",
        "number": "73",
        "set": {
          "id": "swsh4",
          "name": "Sword & Shield?Battle Styles"
        }
      },
      "confidence": 0.98,
      "matchReason": "exact_id_match",
      "matchedFields": ["id", "set.id", "number"]
    }
  ],
  "processingTime": 1234
}
```

---

**Last Updated**: 2025-01-XX  
**Status**: Planning Phase  
**Next Steps**: Review and approve plan, then begin Phase 1 implementation
