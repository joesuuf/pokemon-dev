import { PokemonCard, ApiResponse } from '../types/pokemon';

const API_BASE_URL = '/api';

export class PokemonTCGService {
  private static async makeRequest<T>(endpoint: string): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  static async searchCards(query: string): Promise<ApiResponse> {
    const encodedQuery = encodeURIComponent(query);
    return this.makeRequest<ApiResponse>(`/cards?q=name:${encodedQuery}`);
  }

  static async getCardById(id: string): Promise<{ data: PokemonCard }> {
    return this.makeRequest<{ data: PokemonCard }>(`/cards/${id}`);
  }
}