# OCR Card Identification - Quick Reference

## Feature Summary
Use GCP Vision API to OCR Pokemon card images and match them to official cards with 95% confidence.

## Key Components

### 1. Card ID Locations (Priority Order)
1. **Bottom-Left Corner**: Set symbol + number (e.g., "SM 25/236")
2. **Bottom-Right Corner**: Set code + number (e.g., "swsh4-73")
3. **Card ID Field**: Full ID format (e.g., "swsh4-73")
4. **Set Name**: Fuzzy matching fallback

### 2. API Endpoints
- `POST /api/ocr/upload` - Upload image
- `POST /api/ocr/process` - Run OCR on image
- `POST /api/ocr/match` - Match OCR results to cards

### 3. Matching Strategies (Confidence)
- **Exact ID Match**: 0.98 confidence
- **Set Code + Number**: 0.95 confidence
- **Set Name + Number**: 0.90 confidence
- **Fuzzy Match**: 0.75-0.85 confidence

### 4. Required Dependencies
```json
{
  "@google-cloud/vision": "^4.0.0",
  "react-dropzone": "^14.2.3"
}
```

### 5. Environment Variables
```bash
GCP_VISION_API_KEY=your-api-key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Implementation Timeline
- **Phase 1**: Backend OCR API (Week 1)
- **Phase 2**: Card Matching Logic (Week 1-2)
- **Phase 3**: Frontend UI (Week 2)
- **Phase 4**: Integration & Polish (Week 2-3)

## Cost Estimate
- First 1,000 requests/month: **Free**
- ~$0.0015 per OCR request after that
- Moderate usage (10k/month): ~$13.50/month

## Next Steps
1. Review full plan: `docs/OCR_CARD_IDENTIFICATION_FEATURE_PLAN.md`
2. Set up GCP Vision API credentials
3. Begin Phase 1 implementation
