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

const API_BASE_URL = import.meta.env.VITE_OCR_API_URL || 'http://localhost:3001';

export async function uploadImage(file: File): Promise<OCRUploadResponse> {
  const formData = new FormData();
  formData.append('image', file);

  const response = await fetch(`${API_BASE_URL}/api/ocr/upload`, {
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
  const response = await fetch(`${API_BASE_URL}/api/ocr/process`, {
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
  const response = await fetch(`${API_BASE_URL}/api/ocr/match`, {
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
