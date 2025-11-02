export interface Card {
  id: string
  name: string
  set: string
  cardNumber: string
  image: string
  prices: {
    usd?: number
    usdFoil?: number
    eur?: number
    eurFoil?: number
  }
  links: {
    tcgplayer?: string
    cardmarket?: string
    official?: string
  }
}

export interface PokemonCardPrice {
  low?: number
  mid?: number
  high?: number
  market?: number
  directLow?: number
}

export interface PokemonCardPrices {
  normal?: PokemonCardPrice
  holofoil?: PokemonCardPrice
  reverseHolofoil?: PokemonCardPrice
  '1stEditionHolofoil'?: PokemonCardPrice
  '1stEditionNormal'?: PokemonCardPrice
}

export interface CardmarketPrice {
  averageSellPrice?: number
  lowPrice?: number
  trendPrice?: number
  germanProLow?: number
  suggestedPrice?: number
  reverseHoloSell?: number
  reverseHoloLow?: number
  reverseHoloTrend?: number
  lowPriceExPlus?: number
  avg1?: number
  avg7?: number
  avg30?: number
  reverseHoloAvg1?: number
  reverseHoloAvg7?: number
  reverseHoloAvg30?: number
}

export interface TCGPlayerData {
  url?: string
  updatedAt?: string
  prices?: PokemonCardPrices
}

export interface CardmarketData {
  url?: string
  updatedAt?: string
  prices?: CardmarketPrice
}

export interface PokemonTCGCard {
  id: string
  name: string
  supertype: string
  subtypes: string[]
  level?: string
  hp?: string
  types: string[]
  evolvesFrom?: string
  evolvesTo?: string[]
  rules?: string[]
  abilities?: Array<{
    name: string
    text: string
    type: string
  }>
  attacks?: Array<{
    cost: string[]
    name: string
    text: string
    damage: string
    convertedEnergyCost: number
  }>
  set: {
    id: string
    name: string
    series?: string
    printedTotal?: number
    total?: number
    releaseDate?: string
    images?: {
      symbol?: string
      logo?: string
    }
  }
  cardNumber: string
  artist?: string
  rarity?: string
  images: {
    small: string
    large: string
  }
  tcgplayer?: TCGPlayerData
  cardmarket?: CardmarketData
}

export interface SearchResult {
  data: PokemonTCGCard[]
  page: number
  pageSize: number
  count: number
  totalCount: number
}
