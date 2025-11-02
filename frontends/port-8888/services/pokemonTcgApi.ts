// src/services/pokemonTcgApi.ts
import { SearchParams, ApiResponse } from '../types/pokemon';

// Use the serverless proxy API instead of direct calls
// The proxy handles API key authentication server-side
const PROXY_BASE_URL = '/api';

function formatQuery(params: SearchParams): string {
  const queryParts: string[] = [];
  
  if (params.name) {
    // Check if the user already included field syntax
    if (params.name.includes(':')) {
      queryParts.push(params.name);
    } else {
      // Add wildcards for partial matching
      queryParts.push(`name:*${params.name}*`);
    }
  }
  
  if (params.attackName) {
    // Check if the user already included field syntax
    if (params.attackName.includes(':')) {
      queryParts.push(params.attackName);
    } else {
      queryParts.push(`attacks.name:*${params.attackName}*`);
    }
  }
  
  // Join with AND operator if we have multiple parts
  return queryParts.length > 1 ? queryParts.join(' AND ') : queryParts[0] || '';
}

export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  try {
    console.log('[INFO] Starting search for:', JSON.stringify(params));
    
    const query = formatQuery(params);
    console.log('[DEBUG] Query formatted as:', query);
    
    if (!query) {
      console.warn('[WARNING] Empty query, returning empty results');
      return { data: [], page: 1, pageSize: 20, count: 0, totalCount: 0 };
    }
    
    console.log('[INFO] Calling Pokemon TCG API via proxy...');
    
    const requestUrl = new URL(`${PROXY_BASE_URL}/cards`);
    requestUrl.searchParams.append('q', query);
    requestUrl.searchParams.append('pageSize', '20');
    
    console.log('[DEBUG] Requesting URL:', requestUrl.toString());
    
    const response = await fetch(requestUrl.toString(), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('[ERROR] API Response Error:');
      console.error('[ERROR] Status:', response.status);
      console.error('[ERROR] Status Text:', response.statusText);
      console.error('[ERROR] Data:', errorData);
      
      throw new Error(`API Error (${response.status}): ${errorData.error || response.statusText}`);
    }
    
    const data: ApiResponse = await response.json();
    
    console.log('[SUCCESS] API Response received');
    console.log('[INFO] Found', data.count, 'cards out of', data.totalCount, 'total matches');
    
    if (data.data.length > 0) {
      console.log('[DEBUG] First card:', data.data[0].name);
      console.log('[DEBUG] Card IDs:', data.data.map(c => c.id).join(', '));
    }
    
    return data;
  } catch (error) {
    if (error instanceof Error) {
      console.error('[ERROR] Request failed:', error.message);
      throw error;
    }
    
    console.error('[ERROR] Unexpected error type:', error);
    throw new Error('Unknown error occurred while fetching cards');
  }
}