// src/services/masterlistService.ts
import { PokemonCard, ApiResponse } from '../types/pokemon';

/**
 * Masterlist Service
 * Loads Pokemon card data once and provides local search functionality
 * Instead of making API calls for each search, we search through cached data
 */

let masterlistCache: PokemonCard[] | null = null;
let isLoadingMasterlist = false;
let loadPromise: Promise<PokemonCard[]> | null = null;

/**
 * Fetch all Pokemon cards from the API and cache them
 * This is called once on first search
 */
async function loadMasterlist(): Promise<PokemonCard[]> {
  // If already loading, return the existing promise
  if (loadPromise) {
    return loadPromise;
  }

  // If already cached, return cache
  if (masterlistCache) {
    return masterlistCache;
  }

  // If currently loading, wait for it
  if (isLoadingMasterlist) {
    return loadPromise!;
  }

  isLoadingMasterlist = true;

  loadPromise = (async () => {
    try {
      console.log('[MASTERLIST] Loading Pokemon card masterlist...');
      
      // Use wildcard query to get all cards
      // Fetch with a large pageSize to get as many cards as possible
      const query = encodeURIComponent('name:*');
      const pageSize = 1000; // Large page size to minimize requests

      // Get API key from environment variable
      const apiKey = import.meta.env.VITE_POKEMON_API_KEY || '';
      const apiUrl = 'https://api.pokemontcg.io/v2/cards';
      
      // Build headers with API key if available
      const headers: HeadersInit = {
        'Content-Type': 'application/json',
      };
      if (apiKey) {
        headers['X-Api-Key'] = apiKey;
      }

      const url = `${apiUrl}?q=${query}&pageSize=${pageSize}&orderBy=name`;
      console.log('[MASTERLIST] Fetching from:', url);

      const response = await fetch(url, { headers });

      if (!response.ok) {
        throw new Error(`Failed to load masterlist: ${response.status} ${response.statusText}`);
      }

      const data: ApiResponse = await response.json();
      const allCards = data.data;

      console.log(`[MASTERLIST] Loaded ${allCards.length} cards (total available: ${data.totalCount})`);
      
      // Note: If totalCount > allCards.length, we're only getting a subset
      // This is acceptable for now - searches will work on the cached subset
      if (data.totalCount > allCards.length) {
        console.warn(`[MASTERLIST] Only loaded ${allCards.length} of ${data.totalCount} total cards. Some cards may not be searchable.`);
      }

      masterlistCache = allCards;
      console.log(`[MASTERLIST] Masterlist loaded successfully: ${allCards.length} cards`);
      
      return allCards;
    } catch (error) {
      console.error('[MASTERLIST] Error loading masterlist:', error);
      isLoadingMasterlist = false;
      loadPromise = null;
      throw error;
    } finally {
      isLoadingMasterlist = false;
    }
  })();

  return loadPromise;
}

/**
 * Search through the masterlist for cards matching the search criteria
 */
function searchMasterlist(
  cards: PokemonCard[],
  params: { name?: string; attackName?: string }
): PokemonCard[] {
  let results = cards;

  // Filter by name if provided
  if (params.name) {
    const nameLower = params.name.toLowerCase().trim();
    results = results.filter(card => {
      const cardNameLower = card.name.toLowerCase();
      return cardNameLower.includes(nameLower);
    });
  }

  // Filter by attack name if provided
  if (params.attackName) {
    const attackNameLower = params.attackName.toLowerCase().trim();
    results = results.filter(card => {
      if (!card.attacks || card.attacks.length === 0) {
        return false;
      }
      return card.attacks.some(attack => 
        attack.name.toLowerCase().includes(attackNameLower)
      );
    });
  }

  return results;
}

/**
 * Main search function that uses the masterlist
 */
export async function searchCardsFromMasterlist(
  params: { name?: string; attackName?: string },
  page: number = 1,
  pageSize: number = 20
): Promise<ApiResponse> {
  try {
    console.log('[MASTERLIST] Searching masterlist for:', JSON.stringify(params));

    // Ensure masterlist is loaded
    const masterlist = await loadMasterlist();

    // Search through the masterlist
    let results = searchMasterlist(masterlist, params);

    // Sort results by name for consistency
    results = results.sort((a, b) => {
      const nameCompare = a.name.localeCompare(b.name);
      if (nameCompare !== 0) return nameCompare;
      // If names are equal, sort by number descending
      return parseInt(b.number) - parseInt(a.number);
    });

    const totalCount = results.length;
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const paginatedResults = results.slice(startIndex, endIndex);

    console.log(`[MASTERLIST] Found ${totalCount} total matches, returning page ${page} (${paginatedResults.length} cards)`);

    return {
      data: paginatedResults,
      page,
      pageSize,
      count: paginatedResults.length,
      totalCount,
    };
  } catch (error) {
    console.error('[MASTERLIST] Search error:', error);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred while searching masterlist');
  }
}

/**
 * Clear the masterlist cache (useful for testing or reloading)
 */
export function clearMasterlistCache(): void {
  masterlistCache = null;
  loadPromise = null;
  isLoadingMasterlist = false;
}

/**
 * Get the current masterlist cache size
 */
export function getMasterlistSize(): number {
  return masterlistCache?.length || 0;
}

/**
 * Check if masterlist is loaded
 */
export function isMasterlistLoaded(): boolean {
  return masterlistCache !== null;
}

/**
 * Get a Pokemon card by ID from the masterlist
 */
export async function getCardById(id: string): Promise<PokemonCard | null> {
  const masterlist = await loadMasterlist();
  return masterlist.find(card => card.id === id) || null;
}

/**
 * Get random Pokemon cards from the masterlist
 */
export async function getRandomCards(count: number = 20): Promise<PokemonCard[]> {
  const masterlist = await loadMasterlist();
  
  // Shuffle array and take first N items
  const shuffled = [...masterlist].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

/**
 * Get the image URL for a card, preferring local images if available
 * @param card The Pokemon card
 * @param size 'small' or 'large' - defaults to 'large'
 * @returns URL to the image (local if downloaded, remote otherwise)
 */
export function getCardImageUrl(card: PokemonCard, size: 'small' | 'large' = 'large'): string {
  // Check if image is downloaded locally
  const imageStatus = card.imageStatus?.[size];
  
  if (imageStatus === 'downloaded') {
    // Return local image path
    const cardId = card.id.replace('/', '_').replace('\\', '_');
    return `/images/cards/${cardId}.jpg`;
  }
  
  // Fall back to remote URL
  return card.images[size];
}
