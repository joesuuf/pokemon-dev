import React, { useEffect, useState } from 'react';
import { uploadImage, processOCR, matchCard, type OCRMatchResponse } from '../services/ocrService';

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
