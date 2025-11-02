// src/App.tsx
import { useState, useEffect } from 'react';
import './styles/App.css';
import './components/GridCardItem.css';
import { SearchForm } from './components/SearchForm';
import { CardList } from './components/CardList';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorMessage from './components/ErrorMessage';
import { searchCards } from './services/pokemonTcgApi';
import { PokemonCard, SearchParams } from './types/pokemon';
import { applyRandomGradient } from './utils/gradientUtils';

function App() {
  const [cards, setCards] = useState<PokemonCard[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [timeRemaining, setTimeRemaining] = useState<number>(0);
  const [viewMode, setViewMode] = useState<'card-view' | 'detailed-view'>('card-view');

  // Apply random gradient on component mount
  useEffect(() => {
    applyRandomGradient();
  }, []);

  const handleFormSearch = async (query: string) => {
    const params: SearchParams = {
      name: query
    };
    await handleSearch(params);
  };

  const handleSearch = async (params: SearchParams) => {
    setLoading(true);
    setError(null);
    setTimeRemaining(60);

    // Create a display query for the UI
    const queryParts = [];
    if (params.name) {
      // Check if user already provided field syntax
      if (params.name.includes(':')) {
        queryParts.push(params.name);
      } else {
        queryParts.push(`name:*${params.name}*`);
      }
    }
    if (params.attackName) {
      if (params.attackName.includes(':')) {
        queryParts.push(params.attackName);
      } else {
        queryParts.push(`attacks.name:*${params.attackName}*`);
      }
    }
    const displayQuery = queryParts.join(' AND ');
    setSearchQuery(displayQuery);

    console.log('[INFO] Starting search for:', displayQuery);

    // Start countdown timer
    const timerInterval = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          clearInterval(timerInterval);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    try {
      const response = await searchCards(params);
      clearInterval(timerInterval);
      setCards(response.data);

      if (response.data.length === 0) {
        setError('No cards found matching your search criteria.');
      }
    } catch (err) {
      clearInterval(timerInterval);
      console.error('[ERROR] API Error:', err);

      const errorMessage = err instanceof Error
        ? err.message
        : 'An unexpected error occurred';

      // Provide more user-friendly error messages
      if (errorMessage.includes('timeout')) {
        setError('The search is taking too long. The Pokemon TCG API might be slow or your query might be too complex. Try a simpler search.');
      } else if (errorMessage.includes('400')) {
        setError('Invalid search query. Please check your search syntax.');
      } else if (errorMessage.includes('429')) {
        setError('Too many requests. Please wait a moment and try again.');
      } else {
        setError(errorMessage);
      }

      setCards([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Pokémon TCG Card Search</h1>
        <p className="subtitle">Search for Pokémon cards by name or attack</p>
      </header>

      <main className="app-main">
        <SearchForm
          onSearch={handleFormSearch}
          loading={loading}
          viewMode={viewMode}
          onViewModeChange={setViewMode}
        />

        {searchQuery && (
          <div className="search-query">
            <strong>Search Query:</strong> <code>{searchQuery}</code>
          </div>
        )}

        {loading && <LoadingSpinner timeRemaining={timeRemaining} />}
        {error && <ErrorMessage message={error} />}
        {!loading && !error && cards.length > 0 && (
          <CardList cards={cards} loading={loading} error={error} viewMode={viewMode} />
        )}
      </main>
    </div>
  );
}

export default App;