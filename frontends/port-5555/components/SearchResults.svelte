<script lang="ts">
  import { onMount } from 'svelte';
  import { searchPokemon, getRandomPokemon } from '../lib/api';
  import type { Pokemon } from '../lib/types';
  import PokemonCard from './PokemonCard.svelte';
  import LoadingSpinner from './LoadingSpinner.svelte';

  export let searchQuery: string = '';

  let cards: Pokemon[] = [];
  let loading = false;
  let error: string | null = null;
  let currentPage = 1;
  let totalCount = 0;
  let hasMore = false;

  // Progress tracking
  let loadingProgress = {
    found: 0,
    types: new Set<string>(),
    rarities: new Set<string>(),
    sets: new Set<string>(),
  };

  $: if (searchQuery !== undefined) {
    handleSearch();
  }

  async function handleSearch() {
    loading = true;
    error = null;
    currentPage = 1;
    cards = [];
    
    // Reset progress
    loadingProgress = {
      found: 0,
      types: new Set<string>(),
      rarities: new Set<string>(),
      sets: new Set<string>(),
    };

    try {
      if (searchQuery.trim()) {
        await loadResults();
      } else {
        await loadInitialCards();
      }
    } catch (err) {
      error = err instanceof Error ? err.message : 'An error occurred';
      console.error('Search error:', err);
    } finally {
      loading = false;
    }
  }

  async function loadInitialCards() {
    const results = await getRandomPokemon(20);
    cards = results;
    totalCount = results.length;
    hasMore = false;
    updateProgress(results);
  }

  async function loadResults() {
    const response = await searchPokemon(searchQuery, currentPage);
    cards = response.data;
    totalCount = response.totalCount;
    hasMore = currentPage * 20 < totalCount;
    updateProgress(response.data);
  }

  async function loadMore() {
    if (loading || !hasMore) return;

    loading = true;
    try {
      currentPage += 1;
      const response = await searchPokemon(searchQuery, currentPage);
      
      // Update progress as new cards come in
      updateProgress(response.data);
      
      cards = [...cards, ...response.data];
      hasMore = currentPage * 20 < totalCount;
    } catch (err) {
      error = err instanceof Error ? err.message : 'An error occurred';
    } finally {
      loading = false;
    }
  }

  function updateProgress(newCards: Pokemon[]) {
    loadingProgress.found += newCards.length;
    
    newCards.forEach(card => {
      if (card.types) {
        card.types.forEach(type => loadingProgress.types.add(type));
      }
      if (card.rarity) {
        loadingProgress.rarities.add(card.rarity);
      }
      if (card.set?.name) {
        loadingProgress.sets.add(card.set.name);
      }
    });
    
    // Trigger reactivity
    loadingProgress = loadingProgress;
  }

  onMount(() => {
    handleSearch();
  });
</script>

<div class="search-results">
  {#if loading && cards.length === 0}
    <div class="loading-container">
      <LoadingSpinner />
      {#if loadingProgress.found > 0}
        <div class="progress-info">
          <p class="progress-main">Found {loadingProgress.found} cards!</p>
          {#if loadingProgress.types.size > 0}
            <p class="progress-detail">
              {loadingProgress.types.size} type{loadingProgress.types.size !== 1 ? 's' : ''}: 
              {Array.from(loadingProgress.types).join(', ')}
            </p>
          {/if}
          {#if loadingProgress.rarities.size > 0}
            <p class="progress-detail">
              {loadingProgress.rarities.size} rarity level{loadingProgress.rarities.size !== 1 ? 's' : ''}
            </p>
          {/if}
          {#if loadingProgress.sets.size > 0}
            <p class="progress-detail">
              From {loadingProgress.sets.size} different set{loadingProgress.sets.size !== 1 ? 's' : ''}
            </p>
          {/if}
        </div>
      {/if}
    </div>
  {:else if error}
    <div class="error-message">
      <p>⚠️ {error}</p>
    </div>
  {:else if cards.length === 0}
    <div class="no-results">
      <p>No Pokémon cards found. Try a different search!</p>
    </div>
  {:else}
    <div class="results-header">
      <p class="results-count">
        Showing {cards.length} of {totalCount} cards
      </p>
      {#if loadingProgress.types.size > 0}
        <p class="results-meta">
          Types: {Array.from(loadingProgress.types).slice(0, 5).join(', ')}
          {#if loadingProgress.types.size > 5}
            <span class="more">+{loadingProgress.types.size - 5} more</span>
          {/if}
        </p>
      {/if}
    </div>

    <div class="cards-grid">
      {#each cards as card (card.id)}
        <PokemonCard {card} />
      {/each}
    </div>

    {#if hasMore}
      <div class="load-more-container">
        <button
          class="load-more-btn"
          on:click={loadMore}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Load More'}
        </button>
      </div>
    {/if}
  {/if}
</div>

<style>
  .search-results {
    width: 100%;
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }

  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    gap: 2rem;
  }

  .progress-info {
    text-align: center;
    animation: fadeIn 0.3s ease-in;
  }

  .progress-main {
    font-size: 1.5rem;
    font-weight: bold;
    color: #ffcb05;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  }

  .progress-detail {
    font-size: 1rem;
    color: #ffffff;
    margin: 0.5rem 0;
    opacity: 0.9;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .error-message,
  .no-results {
    text-align: center;
    padding: 3rem;
    font-size: 1.2rem;
    color: #666;
  }

  .error-message p {
    color: #e74c3c;
  }

  .results-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #3b4cca;
  }

  .results-count {
    font-size: 1.2rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 0.5rem;
  }

  .results-meta {
    font-size: 0.9rem;
    color: #666;
  }

  .results-meta .more {
    font-style: italic;
    color: #3b4cca;
  }

  .cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
  }

  .load-more-container {
    display: flex;
    justify-content: center;
    padding: 2rem 0;
  }

  .load-more-btn {
    padding: 1rem 3rem;
    font-size: 1.1rem;
    font-weight: bold;
    color: white;
    background: linear-gradient(135deg, #3b4cca 0%, #2c3e9e 100%);
    border: none;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(59, 76, 202, 0.3);
  }

  .load-more-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59, 76, 202, 0.4);
  }

  .load-more-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  @media (max-width: 768px) {
    .search-results {
      padding: 1rem;
    }

    .cards-grid {
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 1rem;
    }

    .progress-main {
      font-size: 1.2rem;
    }

    .progress-detail {
      font-size: 0.9rem;
    }
  }

  @media (max-width: 480px) {
    .cards-grid {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 0.75rem;
    }
  }
</style>