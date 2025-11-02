// src/App.tsx
import { useState, lazy, Suspense, useEffect, useCallback } from 'react';
import './styles/App.css';
import './components/GridCardItem.css';
import { searchCards } from './services/pokemonTcgApi';
import { PokemonCard, SearchParams } from './types/pokemon';
import { applyRandomGradient } from './utils/gradientUtils';
import { setApiMode as setApiModeConfig, ApiMode } from './config/apiConfig';

// Lazy load components for better performance
const SearchForm = lazy(() => import('./components/SearchForm').then(module => ({ default: module.SearchForm })));
const CardList = lazy(() => import('./components/CardList').then(module => ({ default: module.CardList })));
const LoadingSpinner = lazy(() => import('./components/LoadingSpinner'));
const ErrorMessage = lazy(() => import('./components/ErrorMessage'));
const ApiToggle = lazy(() => import('./components/ApiToggle').then(module => ({ default: module.ApiToggle })));

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

  // Apply random gradient on component mount
  useEffect(() => {
    applyRandomGradient();
  }, []);

  // Handle API mode change
  const handleApiModeChange = useCallback((mode: ApiMode) => {
    setApiModeConfig(mode); // Update config
    console.log(`[APP] API mode changed to: ${mode}`);
    // Clear current results when switching modes
    setCards([]);
    setError(null);
  }, []);

  // SEC-01: Timer cleanup - moved to useEffect to prevent memory leaks
  useEffect(() => {
    let timerInterval: NodeJS.Timeout | null = null;

    if (loading && timeRemaining > 0) {
      timerInterval = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }

    return () => {
      if (timerInterval) {
        clearInterval(timerInterval);
      }
    };
  }, [loading]); // Only depend on loading - timeRemaining updates handled inside

  // PERF-02: Memoize handleSearch callback
  const handleSearch = useCallback(async (params: SearchParams) => {
    setLoading(true);
    setError(null);
    setTimeRemaining(60);

    // Build display query for UI
    const queryParts = [];
    if (params.name) {
      queryParts.push(`Name: ${params.name}`);
    }
    if (params.attackName) {
      queryParts.push(`Attack: ${params.attackName}`);
    }
    const displayQuery = queryParts.join(' AND ');
    setSearchQuery(displayQuery);

    console.log('[INFO] Starting masterlist search for:', displayQuery);

    try {
      const response = await searchCards(params);
      setCards(response.data);

      if (response.data.length === 0) {
        setError('No cards found matching your search criteria.');
      }
    } catch (err) {
      console.error('[ERROR] Search Error:', err);

      const errorMessage = err instanceof Error
        ? err.message
        : 'An unexpected error occurred';

      // Provide user-friendly error messages
      if (errorMessage.includes('Failed to load masterlist')) {
        setError('Failed to load card database. Please check your connection and try again.');
      } else if (errorMessage.includes('API request failed')) {
        setError('Failed to connect to Pokemon TCG API. Please check your connection and try again.');
      } else {
        setError(errorMessage);
      }

      setCards([]);
    } finally {
      setLoading(false);
      setTimeRemaining(0);
    }
  }, []); // Empty deps - uses stable setState functions and imported searchCards

  // PERF-02: Memoize handleFormSearch callback
  const handleFormSearch = useCallback(async (query: string) => {
    const params: SearchParams = {
      name: query
    };
    await handleSearch(params);
  }, [handleSearch]);

  return (
    <div className="app">
      <header className="app-header">
        <h1>Pokémon TCG Card Search</h1>
        <p className="subtitle">Search for Pokémon cards by name or attack</p>
        <Suspense fallback={<div style={{ marginTop: '10px' }}>Loading...</div>}>
          <ApiToggle onModeChange={handleApiModeChange} />
        </Suspense>
      </header>

      <main className="app-main">
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

      {/* Version footer link */}
      <a
        href="/v2/"
        className="version-footer"
        title="Switch to Static HTML/CSS Version"
      >
        Static v2 →
      </a>
    </div>
  );
}

export default App;