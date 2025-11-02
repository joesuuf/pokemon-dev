import express, { Request, Response } from 'express';
import multer from 'multer';
import { v4 as uuidv4 } from 'uuid';
import { ImageAnnotatorClient } from '@google-cloud/vision';
import axios from 'axios';

const router = express.Router();

// Initialize Vision API client (uses GOOGLE_APPLICATION_CREDENTIALS env var)
const visionClient = new ImageAnnotatorClient();

// Configure multer for image uploads
const upload = multer({
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  storage: multer.memoryStorage(),
});

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

interface OCRResults {
  setCode?: string;
  cardNumber?: string;
  fullCardId?: string;
  setName?: string;
}

interface MatchRequest {
  ocrResults: OCRResults;
}

// Parse card text from OCR results
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

// POST /api/ocr/upload - Upload image
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

// POST /api/ocr/process - Process OCR
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
    });

    const detections = result.textAnnotations || [];
    const fullText = detections[0]?.description || '';

    // Extract text from specific regions
    const textRegions: Record<string, string> = {
      fullText,
    };

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
});

// POST /api/ocr/match - Match card
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
      card: any;
      confidence: number;
      matchReason: string;
      matchedFields: string[];
    }> = [];

    // Strategy 1: Exact ID match
    if (ocrResults.fullCardId) {
      try {
        const response = await axios.get(
          `https://api.pokemontcg.io/v2/cards/${ocrResults.fullCardId}`,
          {
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.data?.data) {
          matches.push({
            card: response.data.data,
            confidence: 0.98,
            matchReason: 'exact_id_match',
            matchedFields: ['id'],
          });
        }
      } catch (error) {
        // Continue to next strategy
      }
    }

    // Strategy 2: Set code + number match
    if (ocrResults.setCode && ocrResults.cardNumber && matches.length === 0) {
      try {
        const query = `set.id:${ocrResults.setCode.toLowerCase()} AND number:${ocrResults.cardNumber}`;
        const response = await axios.get(
          `https://api.pokemontcg.io/v2/cards`,
          {
            params: {
              q: query,
              pageSize: 5,
            },
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.data?.data && response.data.data.length > 0) {
          const confidence = response.data.data.length === 1 ? 0.95 : 0.85;
          response.data.data.forEach((card: any) => {
            matches.push({
              card,
              confidence,
              matchReason: 'set_number_match',
              matchedFields: ['set.id', 'number'],
            });
          });
        }
      } catch (error) {
        // Continue to next strategy
      }
    }

    // Strategy 3: Set name + number match (fuzzy)
    if (ocrResults.setName && ocrResults.cardNumber && matches.length === 0) {
      try {
        const query = `set.name:"${ocrResults.setName}" AND number:${ocrResults.cardNumber}`;
        const response = await axios.get(
          `https://api.pokemontcg.io/v2/cards`,
          {
            params: {
              q: query,
              pageSize: 5,
            },
            headers: {
              'X-Api-Key': apiKey,
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.data?.data && response.data.data.length > 0) {
          const confidence = response.data.data.length === 1 ? 0.90 : 0.80;
          response.data.data.forEach((card: any) => {
            matches.push({
              card,
              confidence,
              matchReason: 'set_name_match',
              matchedFields: ['set.name', 'number'],
            });
          });
        }
      } catch (error) {
        // Continue
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
});

export default router;
