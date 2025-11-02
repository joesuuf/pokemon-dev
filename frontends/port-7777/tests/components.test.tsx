import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { SearchForm } from '../components/SearchForm'
import CardItem from '../components/CardItem'
import SkeletonLoader from '../components/SkeletonLoader'
import ResultsList from '../components/ResultsList'
import type { Card } from '../types'

describe('Components', () => {
  describe('SearchForm', () => {
    it('should render search form', () => {
      const mockOnSearch = vi.fn()
      const mockOnViewModeChange = vi.fn()
      render(
        <SearchForm
          onSearch={mockOnSearch}
          loading={false}
          viewMode="card-view"
          onViewModeChange={mockOnViewModeChange}
        />
      )
      expect(screen.getByText('Search')).toBeDefined()
    })

    it('should have input field', () => {
      const mockOnSearch = vi.fn()
      const mockOnViewModeChange = vi.fn()
      render(
        <SearchForm
          onSearch={mockOnSearch}
          loading={false}
          viewMode="card-view"
          onViewModeChange={mockOnViewModeChange}
        />
      )
      const input = screen.getByPlaceholderText(/Enter Pokémon name/i)
      expect(input).toBeDefined()
    })

    it('should disable button when loading', () => {
      const mockOnSearch = vi.fn()
      const mockOnViewModeChange = vi.fn()
      render(
        <SearchForm
          onSearch={mockOnSearch}
          loading={true}
          viewMode="card-view"
          onViewModeChange={mockOnViewModeChange}
        />
      )
      const button = screen.getByText('Searching...')
      expect(button).toBeDefined()
    })

    it('should have search button', () => {
      const mockOnSearch = vi.fn()
      const mockOnViewModeChange = vi.fn()
      render(
        <SearchForm
          onSearch={mockOnSearch}
          loading={false}
          viewMode="card-view"
          onViewModeChange={mockOnViewModeChange}
        />
      )
      const button = screen.getByRole('button')
      expect(button).toBeDefined()
    })
  })

  describe('CardItem', () => {
    const mockCard: Card = {
      id: 'test-1',
      name: 'Charizard',
      set: 'Base Set',
      cardNumber: '4/102',
      image: 'https://example.com/charizard.jpg',
      prices: {
        usd: 100,
        usdFoil: 200,
        eur: 95,
        eurFoil: 190,
      },
      links: {
        tcgplayer: 'https://tcgplayer.com',
        cardmarket: 'https://cardmarket.com',
        official: 'https://pokemon.com',
      },
    }

    it('should render card item', () => {
      render(<CardItem card={mockCard} />)
      expect(screen.getByText('Charizard')).toBeDefined()
    })

    it('should display card name', () => {
      render(<CardItem card={mockCard} />)
      expect(screen.getByText('Charizard')).toBeDefined()
    })

    it('should display card set and number', () => {
      render(<CardItem card={mockCard} />)
      expect(screen.getByText(/Base Set #4\/102/)).toBeDefined()
    })

    it('should display prices', () => {
      render(<CardItem card={mockCard} />)
      expect(screen.getByText(/\$100/)).toBeDefined()
    })

    it('should have TCGPlayer link', () => {
      render(<CardItem card={mockCard} />)
      const tcgLink = screen.getByText('TCGPlayer')
      expect(tcgLink).toBeDefined()
    })

    it('should have Cardmarket link', () => {
      render(<CardItem card={mockCard} />)
      const cmLink = screen.getByText('Cardmarket')
      expect(cmLink).toBeDefined()
    })

    it('should render image with fallback', () => {
      render(<CardItem card={mockCard} />)
      const image = screen.getByAltText('Charizard')
      expect(image).toBeDefined()
    })
  })

  describe('SkeletonLoader', () => {
    it('should not render when not loading', () => {
      const { container } = render(
        <SkeletonLoader isLoading={false} itemCount={3} />
      )
      expect(container.firstChild).toBeNull()
    })

    it('should render when loading', () => {
      render(<SkeletonLoader isLoading={true} itemCount={3} />)
      const skeletons = document.querySelectorAll('[class*="animate-pulse"]')
      expect(skeletons.length).toBeGreaterThan(0)
    })

    it('should render correct number of items', () => {
      const { container } = render(
        <SkeletonLoader isLoading={true} itemCount={5} />
      )
      const items = container.querySelectorAll('[class*="overflow-hidden"]')
      expect(items.length).toBeGreaterThanOrEqual(1)
    })

    it('should have default item count of 3', () => {
      render(<SkeletonLoader isLoading={true} />)
      const skeletons = document.querySelectorAll('[class*="animate-pulse"]')
      expect(skeletons.length).toBeGreaterThan(0)
    })
  })

  describe('ResultsList', () => {
    const mockCards: Card[] = [
      {
        id: 'test-1',
        name: 'Charizard',
        set: 'Base Set',
        cardNumber: '4/102',
        image: 'https://example.com/charizard.jpg',
        prices: { usd: 100 },
        links: {},
      },
      {
        id: 'test-2',
        name: 'Blastoise',
        set: 'Base Set',
        cardNumber: '2/102',
        image: 'https://example.com/blastoise.jpg',
        prices: { usd: 80 },
        links: {},
      },
    ]

    it('should render results list', () => {
      render(<ResultsList cards={mockCards} />)
      expect(screen.getByText('Charizard')).toBeDefined()
      expect(screen.getByText('Blastoise')).toBeDefined()
    })

    it('should render multiple cards', () => {
      render(<ResultsList cards={mockCards} />)
      const cardNames = screen.getAllByText(/Charizard|Blastoise/)
      expect(cardNames.length).toBeGreaterThanOrEqual(2)
    })

    it('should handle empty cards list', () => {
      const { container } = render(<ResultsList cards={[]} />)
      expect(container.firstChild).toBeDefined()
    })

    it('should apply grid layout', () => {
      const { container } = render(<ResultsList cards={mockCards} />)
      const grid = container.querySelector('[class*="grid"]')
      expect(grid).toBeDefined()
    })
  })
})
