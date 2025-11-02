// src/services/pokemonTcgApi.ts
import { SearchParams, ApiResponse } from '../types/pokemon';
import { searchCardsFromMasterlist } from './masterlistService';
import { searchCardsDirect } from './pokemonTcgApiDirect';
import { useDirectApi, useMasterlistApi } from '../config/apiConfig';

/**
 * Unified search function that uses either direct API or masterlist based on configuration
 */
export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  try {
    console.log('[API] Starting search for:', JSON.stringify(params));
    
    // Validate search parameters
    if (!params.name && !params.attackName) {
      console.warn('[API] Empty query, returning empty results');
      return { data: [], page: 1, pageSize: 20, count: 0, totalCount: 0 };
    }
    
    // Choose API mode based on configuration
    if (useDirectApi()) {
      console.log('[API] Using DIRECT API mode');
      return await searchCardsDirect(params, 1, 20);
    } else if (useMasterlistApi()) {
      console.log('[API] Using MASTERLIST mode');
      return await searchCardsFromMasterlist(params, 1, 20);
    } else {
      // Fallback to direct API
      console.warn('[API] Unknown mode, falling back to direct API');
      return await searchCardsDirect(params, 1, 20);
    }
  } catch (error) {
    if (error instanceof Error) {
      console.error('[API] Search failed:', error.message);
      throw error;
    }
    
    console.error('[API] Unexpected error type:', error);
    throw new Error('Unknown error occurred while searching cards');
  }
}