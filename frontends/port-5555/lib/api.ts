import type { Pokemon, PokemonListResponse } from './types';

// Use the serverless proxy API for search queries
// The proxy handles API key authentication server-side
const PROXY_BASE_URL = '/api';
// Direct API calls for endpoints not supported by proxy (public access allowed)
const API_BASE_URL = 'https://api.pokemontcg.io/v2';

const headers: HeadersInit = {
  'Content-Type': 'application/json',
};

export async function searchPokemon(
  query: string,
  page: number = 1,
  pageSize: number = 20
): Promise<PokemonListResponse> {
  const searchQuery = query.trim() 
    ? `name:"${query}*" OR name:"*${query}*"` 
    : '';
  
  const params = new URLSearchParams({
    q: searchQuery,
    page: page.toString(),
    pageSize: pageSize.toString(),
    orderBy: 'name,-number', // Order by name ascending, then number descending
  });

  const response = await fetch(
    `${PROXY_BASE_URL}/cards?${params}`,
    { method: 'GET', headers }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch Pokemon cards');
  }

  return response.json();
}

export async function getPokemonById(id: string): Promise<Pokemon> {
  const response = await fetch(
    `${API_BASE_URL}/cards/${id}`,
    { method: 'GET', headers }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch Pokemon card');
  }

  const data = await response.json();
  return data.data;
}

export async function getRandomPokemon(count: number = 20): Promise<Pokemon[]> {
  const response = await fetch(
    `${API_BASE_URL}/cards?pageSize=${count}&orderBy=name,-number`,
    { method: 'GET', headers }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch random Pokemon cards');
  }

  const data: PokemonListResponse = await response.json();
  return data.data;
}