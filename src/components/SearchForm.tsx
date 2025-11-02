import React, { useState, useCallback } from 'react';

interface SearchFormProps {
  onSearch: (query: string) => void;
  loading: boolean;
  viewMode: 'card-view' | 'detailed-view';
  onViewModeChange: (mode: 'card-view' | 'detailed-view') => void;
}

// PERF-01: Memoize SearchForm component to prevent unnecessary re-renders
export const SearchForm = React.memo<SearchFormProps>(({
  onSearch,
  loading,
  viewMode,
  onViewModeChange
}) => {
  const [query, setQuery] = useState('');

  // PERF-02: Memoize handleSubmit callback
  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  }, [query, onSearch]);

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <div className="form-group">
        <label htmlFor="pokemon-search">search:</label>
        <input
          id="pokemon-search"
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter Pokémon name (e.g., Charizard, Pikachu)"
          disabled={loading}
          className="search-input"
        />
      </div>

      <div className="form-group view-mode-group">
        <label>View Mode:</label>
        <div className="radio-group">
          <label className="radio-label">
            <input
              type="radio"
              name="viewMode"
              value="card-view"
              checked={viewMode === 'card-view'}
              onChange={(e) => onViewModeChange(e.target.value as 'card-view' | 'detailed-view')}
              disabled={loading}
            />
            <span>Card Grid View</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              name="viewMode"
              value="detailed-view"
              checked={viewMode === 'detailed-view'}
              onChange={(e) => onViewModeChange(e.target.value as 'card-view' | 'detailed-view')}
              disabled={loading}
            />
            <span>Detailed List View</span>
          </label>
        </div>
      </div>

      <button type="submit" disabled={loading || !query.trim()} className="search-button">
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
});