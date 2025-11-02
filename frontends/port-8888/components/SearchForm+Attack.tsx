import React, { useState } from 'react';
import { SearchParams } from '../types/pokemon';

interface SearchFormWithAttackProps {
  onSearch: (params: SearchParams) => void;
  loading: boolean;
}

export const SearchFormWithAttack: React.FC<SearchFormWithAttackProps> = ({ onSearch, loading }) => {
  const [cardName, setCardName] = useState('');
  const [attackName, setAttackName] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const params: SearchParams = {};

    if (cardName.trim()) {
      params.name = cardName.trim();
    }

    if (attackName.trim()) {
      params.attackName = attackName.trim();
    }

    if (Object.keys(params).length > 0) {
      onSearch(params);
    }
  };

  const isSearchDisabled = loading || (!cardName.trim() && !attackName.trim());

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="form-group">
        <label htmlFor="pokemon-name">Card Name:</label>
        <input
          id="pokemon-name"
          type="text"
          value={cardName}
          onChange={(e) => setCardName(e.target.value)}
          placeholder="Enter Pokémon name (e.g., Charizard, Pikachu)"
          disabled={loading}
          className="search-input"
        />
      </div>

      <div className="form-group">
        <label htmlFor="attack-name">Attack Name:</label>
        <input
          id="attack-name"
          type="text"
          value={attackName}
          onChange={(e) => setAttackName(e.target.value)}
          placeholder="Enter attack name (e.g., Flamethrower, Thunder)"
          disabled={loading}
          className="search-input"
        />
      </div>

      <p style={{ fontSize: '0.9rem', color: '#003DA5', marginBottom: '15px', fontWeight: '600', letterSpacing: '0.5px' }}>
        {cardName.trim() && attackName.trim() && '🔍 Searching by BOTH card name AND attack'}
        {cardName.trim() && !attackName.trim() && '🔍 Searching by CARD NAME'}
        {!cardName.trim() && attackName.trim() && '⚡ Searching by ATTACK'}
      </p>

      <button type="submit" disabled={isSearchDisabled} className="search-button">
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
};
