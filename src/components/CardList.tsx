import React from 'react';
import { PokemonCard } from '../types/pokemon';
import { CardDisplay } from './CardDisplay';
import { GridCardItem } from './GridCardItem';

interface CardListProps {
  cards: PokemonCard[];
  loading: boolean;
  error: string | null;
  viewMode: 'card-view' | 'detailed-view';
}

// PERF-01: Memoize CardList component to prevent unnecessary re-renders
export const CardList = React.memo<CardListProps>(({ cards, loading, error, viewMode }) => {
  if (loading) {
    return (
      <div className="loading">
        <p>Loading Pokémon cards...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error">
        <p>Error: {error}</p>
      </div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="no-results">
        <p>No Pokémon cards found. Try a different search term.</p>
      </div>
    );
  }

  if (viewMode === 'card-view') {
    return (
      <div className="card-list-grid">
        <h2>Found {cards.length} card(s)</h2>
        <div className="card-grid">
          {cards.map((card) => (
            <GridCardItem key={card.id} card={card} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="card-list">
      <h2>Found {cards.length} card(s)</h2>
      {cards.map((card) => (
        <CardDisplay key={card.id} card={card} />
      ))}
    </div>
  );
});