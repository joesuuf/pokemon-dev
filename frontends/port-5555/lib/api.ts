import type { Pokemon, PokemonListResponse } from './types';

const API_BASE_URL = 'https://api.pokemontcg.io/v2';
const API_KEY = import.meta.env.VITE_POKEMON_TCG_API_KEY;

const headers: HeadersInit = {
  'X-Api-Key': API_KEY || '',
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
    `${API_BASE_URL}/cards?${params}`,
    { headers }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch Pokemon cards');
  }

  return response.json();
}

export async function getPokemonById(id: string): Promise<Pokemon> {
  const response = await fetch(
    `${API_BASE_URL}/cards/${id}`,
    { headers }
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
    { headers }
  );

  if (!response.ok) {
    throw new Error('Failed to fetch random Pokemon cards');
  }

  const data: PokemonListResponse = await response.json();
  return data.data;
}