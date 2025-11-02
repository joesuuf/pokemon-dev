// src/App.tsx
import { useState, lazy, Suspense } from 'react';
import './styles/App.css';
import './components/GridCardItem.css';
import { searchCards } from './services/pokemonTcgApi';
import { PokemonCard, SearchParams } from './types/pokemon';

// Lazy load components for better performance
const SearchForm = lazy(() => import('./components/SearchForm').then(module => ({ default: module.SearchForm })));
const CardList = lazy(() => import('./components/CardList').then(module => ({ default: module.CardList })));
const LoadingSpinner = lazy(() => import('./components/LoadingSpinner'));
const ErrorMessage = lazy(() => import('./components/ErrorMessage'));
const CloudflareStreamVideo = lazy(() => import('./components/CloudflareStreamVideo').then(module => ({ default: module.CloudflareStreamVideo })));

// Simple fallback component for Suspense
const ComponentLoader = () => (
  <div style={{ padding: '20px', textAlign: 'center' }}>
    <div className="loading-spinner">Loading...</div>
  </div>
);

function App() {
  const [cards, setCards] = useState<PokemonCard[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [timeRemaining, setTimeRemaining] = useState<number>(0);
  const [viewMode, setViewMode] = useState<'card-view' | 'detailed-view'>('card-view');

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
        <div className="video-section" style={{ marginBottom: '2rem', maxWidth: '800px', margin: '0 auto 2rem auto' }}>
          <Suspense fallback={<ComponentLoader />}>
            <CloudflareStreamVideo videoId="8b2c797f471c0126be3dad81cd59d609" />
          </Suspense>
        </div>

        <Suspense fallback={<ComponentLoader />}>
          <SearchForm
            onSearch={handleFormSearch}
            loading={loading}
            viewMode={viewMode}
            onViewModeChange={setViewMode}
          />
        </Suspense>

        {searchQuery && (
          <div className="search-query">
            <strong>Search Query:</strong> <code>{searchQuery}</code>
          </div>
        )}

        {loading && (
          <Suspense fallback={<ComponentLoader />}>
            <LoadingSpinner timeRemaining={timeRemaining} />
          </Suspense>
        )}
        {error && (
          <Suspense fallback={<ComponentLoader />}>
            <ErrorMessage message={error} />
          </Suspense>
        )}
        {!loading && !error && cards.length > 0 && (
          <Suspense fallback={<ComponentLoader />}>
            <CardList cards={cards} loading={loading} error={error} viewMode={viewMode} />
          </Suspense>
        )}
      </main>
    </div>
  );
}

export default App;