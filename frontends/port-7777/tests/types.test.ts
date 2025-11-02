import { describe, it, expect } from 'vitest'
import type {
  Card,
  PokemonTCGCard,
  SearchResult,
  TCGPlayerData,
  CardmarketData,
} from '../types'

describe('Types', () => {
  describe('Card type', () => {
    it('should have required properties', () => {
      const card: Card = {
        id: 'test-id',
        name: 'Charizard',
        set: 'Base Set',
        cardNumber: '4/102',
        image: 'https://example.com/image.jpg',
        prices: {
          usd: 100.0,
          usdFoil: 200.0,
          eur: 90.0,
          eurFoil: 180.0,
        },
        links: {
          tcgplayer: 'https://tcgplayer.com',
          cardmarket: 'https://cardmarket.com',
          official: 'https://pokemon.com',
        },
      }
      expect(card.id).toBeDefined()
      expect(card.name).toBeDefined()
      expect(card.set).toBeDefined()
      expect(card.cardNumber).toBeDefined()
      expect(card.image).toBeDefined()
      expect(card.prices).toBeDefined()
      expect(card.links).toBeDefined()
    })

    it('should allow optional price fields', () => {
      const card: Card = {
        id: 'test-id',
        name: 'Pikachu',
        set: 'Base Set',
        cardNumber: '25/102',
        image: '',
        prices: {},
        links: {},
      }
      expect(card.prices).toEqual({})
    })

    it('should allow optional link fields', () => {
      const card: Card = {
        id: 'test-id',
        name: 'Blastoise',
        set: 'Base Set',
        cardNumber: '2/102',
        image: '',
        prices: { usd: 50 },
        links: { tcgplayer: 'https://example.com' },
      }
      expect(card.links.cardmarket).toBeUndefined()
    })
  })

  describe('PokemonTCGCard type', () => {
    it('should have required properties', () => {
      const apiCard: PokemonTCGCard = {
        id: 'base1-4',
        name: 'Charizard',
        supertype: 'Pokémon',
        subtypes: ['Stage 2'],
        types: ['Fire'],
        cardNumber: '4',
        set: {
          id: 'base1',
          name: 'Base Set',
        },
        images: {
          small: 'https://example.com/small.jpg',
          large: 'https://example.com/large.jpg',
        },
      }
      expect(apiCard.id).toBeDefined()
      expect(apiCard.name).toBeDefined()
      expect(apiCard.supertype).toBeDefined()
      expect(apiCard.images).toBeDefined()
    })

    it('should allow optional TCG player data', () => {
      const tcgData: TCGPlayerData = {
        url: 'https://tcgplayer.com/product/1234',
        prices: {
          normal: {
            market: 100.0,
          },
        },
      }
      expect(tcgData.url).toBeDefined()
      expect(tcgData.prices).toBeDefined()
    })

    it('should allow optional cardmarket data', () => {
      const cardmarketData: CardmarketData = {
        url: 'https://cardmarket.com/product/1234',
        prices: {
          averageSellPrice: 95.0,
          trendPrice: 90.0,
        },
      }
      expect(cardmarketData.url).toBeDefined()
      expect(cardmarketData.prices).toBeDefined()
    })
  })

  describe('SearchResult type', () => {
    it('should have required properties', () => {
      const result: SearchResult = {
        data: [],
        page: 1,
        pageSize: 20,
        count: 0,
        totalCount: 0,
      }
      expect(result.data).toBeDefined()
      expect(result.page).toBe(1)
      expect(result.pageSize).toBe(20)
      expect(result.count).toBe(0)
      expect(result.totalCount).toBe(0)
    })

    it('should contain array of PokemonTCGCard', () => {
      const cards: PokemonTCGCard[] = [
        {
          id: 'base1-4',
          name: 'Charizard',
          supertype: 'Pokémon',
          subtypes: ['Stage 2'],
          types: ['Fire'],
          cardNumber: '4',
          set: { id: 'base1', name: 'Base Set' },
          images: {
            small: 'https://example.com/small.jpg',
            large: 'https://example.com/large.jpg',
          },
        },
      ]
      const result: SearchResult = {
        data: cards,
        page: 1,
        pageSize: 1,
        count: 1,
        totalCount: 1,
      }
      expect(result.data).toHaveLength(1)
      expect(result.data[0].name).toBe('Charizard')
    })
  })
})
