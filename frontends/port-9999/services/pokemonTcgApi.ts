// src/services/pokemonTcgApi.ts
import axios, { AxiosError } from 'axios';
import { SearchParams, ApiResponse } from '../types/pokemon';

const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;
const BASE_URL = 'https://api.pokemontcg.io/v2';

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    ...(API_KEY && { 'X-Api-Key': API_KEY })
  },
  timeout: 60000
});

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
    
    console.log('[INFO] Calling Pokemon TCG API...');
    
    const requestUrl = `${BASE_URL}/cards?q=${encodeURIComponent(query)}&pageSize=20`;
    console.log('[DEBUG] Requesting URL:', requestUrl);
    console.log('[DEBUG] Using API Key:', API_KEY ? 'Yes' : 'No (public access)');
    
    const requestParams = {
      q: query,
      pageSize: 20
    };
    
    console.log('[DEBUG] Request: GET', `${BASE_URL}/cards`);
    console.log('[DEBUG] Params:', requestParams);
    
    const response = await axiosInstance.get<ApiResponse>('/cards', {
      params: requestParams
    });
    
    console.log('[SUCCESS] API Response received');
    console.log('[INFO] Found', response.data.count, 'cards out of', response.data.totalCount, 'total matches');
    
    if (response.data.data.length > 0) {
      console.log('[DEBUG] First card:', response.data.data[0].name);
      console.log('[DEBUG] Card IDs:', response.data.data.map(c => c.id).join(', '));
    }
    
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError;
      
      if (!axiosError.response) {
        console.error('[ERROR] No response from server:', axiosError.response || {});
        console.error('[ERROR] Network/Request error:', axiosError.message);
        
        if (axiosError.code === 'ECONNABORTED') {
          console.error('[ERROR] Request timeout - API may be slow or unreachable');
        }
      } else {
        console.error('[ERROR] API Response Error:');
        console.error('[ERROR] Status:', axiosError.response.status);
        console.error('[ERROR] Status Text:', axiosError.response.statusText);
        console.error('[ERROR] Data:', axiosError.response.data);
        console.error('[ERROR] Headers:', axiosError.response.headers);
      }
      
      console.error('[ERROR] No response received from server');
      throw new Error(`API Error (${axiosError.response?.status || 'N/A'}): ${axiosError.message}`);
    }
    
    console.error('[ERROR] Unexpected error type:', error);
    throw error;
  }
}