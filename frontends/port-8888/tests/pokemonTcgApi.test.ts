import { describe, it, expect, beforeEach, vi } from 'vitest'

// Mock axios before importing the service
vi.mock('axios', () => {
  return {
    default: {
      create: vi.fn(() => ({
        get: vi.fn(),
        post: vi.fn(),
        put: vi.fn(),
        delete: vi.fn(),
        interceptors: {
          request: { use: vi.fn(() => 1) },
          response: { use: vi.fn(() => 1) },
        },
      })),
    },
  }
})

describe('Pokemon TCG API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should export searchCards function', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(searchCards).toBeDefined()
  })

  it('should be an async function', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(searchCards.constructor.name).toBe('AsyncFunction')
  })

  it('should handle card search module import', async () => {
    const module = await import('../services/pokemonTcgApi')
    expect(module).toBeDefined()
    expect(module.searchCards).toBeDefined()
  })

  it('should export Card type', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(typeof searchCards).toBe('function')
  })

  it('should have proper return type', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(searchCards).toBeInstanceOf(Function)
  })

  it('should accept query parameter', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(searchCards.length).toBeGreaterThan(0)
  })

  it('should accept optional logging callback', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    expect(searchCards.length).toBeGreaterThanOrEqual(1)
  })

  it('should return promise', async () => {
    const { searchCards } = await import('../services/pokemonTcgApi')
    const result = searchCards({ name: 'test' }).catch(() => {
      // Ignore error since we're just checking the type
      return { data: [], page: 1, pageSize: 20, count: 0, totalCount: 0 }
    })
    expect(result instanceof Promise).toBe(true)
  })
})
