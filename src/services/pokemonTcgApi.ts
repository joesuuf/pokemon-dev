// src/services/pokemonTcgApi.ts
import { SearchParams, ApiResponse } from '../types/pokemon';
import { searchCardsFromMasterlist } from './masterlistService';

/**
 * Search Pokemon cards using the masterlist instead of API calls
 * This provides faster, offline-capable searches once the masterlist is loaded
 */
export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  try {
    console.log('[INFO] Starting search for:', JSON.stringify(params));
    
    // Validate search parameters
    if (!params.name && !params.attackName) {
      console.warn('[WARNING] Empty query, returning empty results');
      return { data: [], page: 1, pageSize: 20, count: 0, totalCount: 0 };
    }
    
    console.log('[INFO] Searching masterlist...');
    
    // Use masterlist service for search
    const data = await searchCardsFromMasterlist(params, 1, 20);
    
    console.log('[SUCCESS] Masterlist search completed');
    console.log('[INFO] Found', data.count, 'cards out of', data.totalCount, 'total matches');
    
    if (data.data.length > 0) {
      console.log('[DEBUG] First card:', data.data[0].name);
      console.log('[DEBUG] Card IDs:', data.data.map(c => c.id).join(', '));
    }
    
    return data;
  } catch (error) {
    if (error instanceof Error) {
      console.error('[ERROR] Search failed:', error.message);
      throw error;
    }
    
    console.error('[ERROR] Unexpected error type:', error);
    throw new Error('Unknown error occurred while searching cards');
  }
}