import React, { useState } from 'react';
import { ImageUpload } from '../components/ImageUpload';
import { OCRProcessing } from '../components/OCRProcessing';
import { CardMatchResult } from '../components/CardMatchResult';
import type { OCRMatchResponse } from '../services/ocrService';
import type { PokemonCard } from '../types/pokemon';

export const OCRSearch: React.FC = () => {
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

  const handleSelectCard = (card: PokemonCard) => {
    // Navigate to card details or show modal
    console.log('Selected card:', card);
    // You can add navigation logic here
    window.open(`https://pokemontcg.io/cards/${card.id}`, '_blank');
  };

  return (
    <div className="container mx-auto p-4 space-y-6 max-w-4xl">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-2">OCR Card Search</h1>
        <p className="text-gray-600">
          Upload an image of a Pokemon card to identify it automatically
        </p>
      </div>
      
      <ImageUpload onImageSelect={handleImageSelect} />

      {processing && imageFile && (
        <div className="bg-white p-6 rounded-lg shadow">
          <OCRProcessing
            imageFile={imageFile}
            onComplete={handleComplete}
            onError={handleError}
          />
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded text-red-700">
          <strong>Error:</strong> {error}
        </div>
      )}

      {results && (
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">
            Found {results.matches.length} match(es)
          </h2>
          {results.matches.length === 0 ? (
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded text-yellow-700">
              No matches found with 95%+ confidence. Try uploading a clearer image.
            </div>
          ) : (
            results.matches.map((match, index) => (
              <CardMatchResult
                key={index}
                match={match}
                onSelect={handleSelectCard}
              />
            ))
          )}
        </div>
      )}
    </div>
  );
};
