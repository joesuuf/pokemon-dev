// src/services/pokemonTcgApiDirect.ts
/**
 * Direct Pokemon TCG API Service
 * Makes direct API calls to Pokemon TCG API for each search
 * Slower but always up-to-date, no caching needed
 */

import { SearchParams, ApiResponse } from '../types/pokemon';

/**
 * Build query string for Pokemon TCG API
 */
function buildQuery(params: SearchParams): string {
  const queryParts: string[] = [];
  
  if (params.name) {
    queryParts.push(`name:"*${params.name}*"`);
  }
  
  if (params.attackName) {
    queryParts.push(`attacks.name:"*${params.attackName}*"`);
  }
  
  return queryParts.join(' AND ') || '*';
}

/**
 * Search Pokemon cards directly from Pokemon TCG API
 */
export async function searchCardsDirect(
  params: SearchParams,
  page: number = 1,
  pageSize: number = 20
): Promise<ApiResponse> {
  try {
    console.log('[DIRECT API] Starting search for:', JSON.stringify(params));
    
    // Validate search parameters
    if (!params.name && !params.attackName) {
      console.warn('[DIRECT API] Empty query, returning empty results');
      return { data: [], page, pageSize, count: 0, totalCount: 0 };
    }
    
    // Build query string
    const query = buildQuery(params);
    const encodedQuery = encodeURIComponent(query);
    
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
    
    // Build URL with query parameters
    const url = `${apiUrl}?q=${encodedQuery}&page=${page}&pageSize=${pageSize}&orderBy=name`;
    console.log('[DIRECT API] Fetching from:', url);
    
    const response = await fetch(url, { headers });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}. ${errorText}`
      );
    }
    
    const data: ApiResponse = await response.json();
    
    console.log(`[DIRECT API] Found ${data.count} cards (page ${page} of ${Math.ceil((data.totalCount || 0) / pageSize)})`);
    console.log(`[DIRECT API] Total matches: ${data.totalCount || 0}`);
    
    return data;
  } catch (error) {
    console.error('[DIRECT API] Search error:', error);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred while searching cards via direct API');
  }
}

/**
 * Get a Pokemon card by ID directly from API
 */
export async function getCardByIdDirect(id: string): Promise<ApiResponse> {
  try {
    const apiKey = import.meta.env.VITE_POKEMON_API_KEY || '';
    const apiUrl = `https://api.pokemontcg.io/v2/cards/${id}`;
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    if (apiKey) {
      headers['X-Api-Key'] = apiKey;
    }
    
    const response = await fetch(apiUrl, { headers });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch card: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    return {
      data: [data.data],
      page: 1,
      pageSize: 1,
      count: 1,
      totalCount: 1,
    };
  } catch (error) {
    console.error('[DIRECT API] Get card by ID error:', error);
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Unknown error occurred while fetching card');
  }
}
