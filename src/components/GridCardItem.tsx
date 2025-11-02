import React, { useState, useCallback } from 'react';
import { PokemonCard } from '../types/pokemon';
import { CardDisplay } from './CardDisplay';

interface GridCardItemProps {
  card: PokemonCard;
}

// PERF-01: Memoize GridCardItem component to prevent unnecessary re-renders
export const GridCardItem = React.memo<GridCardItemProps>(({ card }) => {
  const [showDetails, setShowDetails] = useState(false);

  // PERF-02: Memoize callback handlers
  const handleShowDetails = useCallback(() => {
    setShowDetails(true);
  }, []);

  const handleHideDetails = useCallback(() => {
    setShowDetails(false);
  }, []);

  if (showDetails) {
    return (
      <div className="card-grid-item-expanded">
        <button
          className="card-close-btn"
          onClick={handleHideDetails}
          title="Close details"
        >
          ✕
        </button>
        <CardDisplay card={card} />
      </div>
    );
  }

  return (
    <div className="card-grid-item" onClick={handleShowDetails}>
      <div className="card-grid-image">
        <img
          src={card.images.small}
          alt={card.name}
          loading="lazy"
          onError={(e) => {
            (e.target as HTMLImageElement).src =
              'https://via.placeholder.com/120x168?text=Card+Not+Found';
          }}
        />
      </div>
      <div className="card-grid-info">
        <h3 className="card-grid-name">{card.name}</h3>
        <p className="card-grid-set">
          {card.set.name} #{card.number}
        </p>
        <p className="card-grid-type">{card.supertype}</p>
        <button className="card-view-btn">View Details</button>
      </div>
    </div>
  );
});
