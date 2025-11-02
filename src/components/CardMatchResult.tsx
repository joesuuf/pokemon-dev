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
