/**
 * TypeScript Type Definitions for Pokemon TCG API
 *
 * These types match the Pokemon TCG API v2 response structure
 * API Documentation: https://pokemontcg.io/
 */

/**
 * Pokemon Card Image URLs
 */
export interface CardImage {
  small: string;
  large: string;
}

/**
 * Set information
 */
export interface CardSet {
  id: string;
  name: string;
  series: string;
  printedTotal?: number;
  total: number;
  releaseDate?: string;
  updatedAt?: string;
  images?: {
    symbol: string;
    logo: string;
  };
}

/**
 * Attack information
 */
export interface Attack {
  name: string;
  cost: string[];
  convertedEnergyCost: number;
  damage: string;
  text: string;
}

/**
 * Ability information
 */
export interface Ability {
  name: string;
  text: string;
  type: string;
}

/**
 * Weakness information
 */
export interface Weakness {
  type: string;
  value: string;
}

/**
 * Resistance information
 */
export interface Resistance {
  type: string;
  value: string;
}

/**
 * TCGPlayer price information
 */
export interface PriceInfo {
  low?: number;
  mid?: number;
  high?: number;
  market?: number;
  directLow?: number;
}

/**
 * TCGPlayer pricing data
 */
export interface TCGPlayer {
  url: string;
  updatedAt: string;
  prices?: {
    normal?: PriceInfo;
    holofoil?: PriceInfo;
    reverseHolofoil?: PriceInfo;
    '1stEditionHolofoil'?: PriceInfo;
    '1stEditionNormal'?: PriceInfo;
    [key: string]: PriceInfo | undefined;
  };
}

/**
 * Cardmarket pricing data
 */
export interface CardMarket {
  url: string;
  updatedAt: string;
  prices?: {
    averageSellPrice?: number;
    lowPrice?: number;
    trendPrice?: number;
    germanProLow?: number;
    suggestedPrice?: number;
    reverseHoloSell?: number;
    reverseHoloLow?: number;
    reverseHoloTrend?: number;
    lowPriceExPlus?: number;
    avg1?: number;
    avg7?: number;
    avg30?: number;
    reverseHoloAvg1?: number;
    reverseHoloAvg7?: number;
    reverseHoloAvg30?: number;
  };
}

/**
 * Legalities for different formats
 */
export interface Legalities {
  unlimited?: string;
  standard?: string;
  expanded?: string;
}

/**
 * Complete Pokemon Card
 */
export interface PokemonCard {
  id: string;
  name: string;
  supertype: string;
  subtypes?: string[];
  level?: string;
  hp?: string;
  types?: string[];
  evolvesFrom?: string;
  evolvesTo?: string[];
  rules?: string[];
  ancientTrait?: {
    name: string;
    text: string;
  };
  abilities?: Ability[];
  attacks?: Attack[];
  weaknesses?: Weakness[];
  resistances?: Resistance[];
  retreatCost?: string[];
  convertedRetreatCost?: number;
  set: CardSet;
  number: string;
  artist?: string;
  rarity?: string;
  flavorText?: string;
  nationalPokedexNumbers?: number[];
  legalities?: Legalities;
  regulationMark?: string;
  images: CardImage;
  imageStatus?: {
    large?: 'downloaded' | 'missing' | 'needed' | 'error';
    small?: 'downloaded' | 'missing' | 'needed' | 'error';
    updatedAt?: string;
  };
  tcgplayer?: TCGPlayer;
  cardmarket?: CardMarket;
}

/**
 * API Response for card search
 */
export interface CardSearchResponse {
  data: PokemonCard[];
  page: number;
  pageSize: number;
  count: number;
  totalCount: number;
}

/**
 * API Response for single card
 */
export interface SingleCardResponse {
  data: PokemonCard;
}

/**
 * API Error response
 */
export interface ApiError {
  message: string;
  errors?: string[];
}

/**
 * Search parameters for API queries
 */
export interface SearchParams {
  q?: string;
  page?: number;
  pageSize?: number;
  orderBy?: string;
  select?: string;
}

/**
 * View mode for card display
 */
export type ViewMode = 'list' | 'grid' | '3col';

/**
 * Type aliases for backward compatibility with existing code
 */
export type Pokemon = PokemonCard;
export type PokemonListResponse = CardSearchResponse;
