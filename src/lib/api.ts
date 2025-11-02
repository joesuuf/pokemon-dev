import type { Pokemon, PokemonListResponse } from './types';
import { searchCardsFromMasterlist, getCardById as getCardByIdFromMasterlist, getRandomCards as getRandomCardsFromMasterlist } from '../services/masterlistService';

/**
 * Search Pokemon cards using the masterlist
 */
export async function searchPokemon(
  query: string,
  page: number = 1,
  pageSize: number = 20
): Promise<PokemonListResponse> {
  if (!query.trim()) {
    return { data: [], page, pageSize, count: 0, totalCount: 0 };
  }

  const params = {
    name: query.trim()
  };

  return searchCardsFromMasterlist(params, page, pageSize);
}

/**
 * Get a Pokemon card by ID from the masterlist
 */
export async function getPokemonById(id: string): Promise<Pokemon> {
  const card = await getCardByIdFromMasterlist(id);
  
  if (!card) {
    throw new Error(`Pokemon card with ID ${id} not found`);
  }

  return card;
}

/**
 * Get random Pokemon cards from the masterlist
 */
export async function getRandomPokemon(count: number = 20): Promise<Pokemon[]> {
  return getRandomCardsFromMasterlist(count);
}
