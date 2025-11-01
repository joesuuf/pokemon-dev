# Proposed Robust Performance Implementation Plan

**Project:** Pokemon TCG Search Application
**Plan Date:** October 31, 2025
**Last Updated:** November 1, 2025
**Branch:** main (originally created on: claude/performance-audit-011CUfQhreP1hvQQK9FDsnXH)

## Executive Summary

This document outlines a comprehensive, phased approach to transforming the Pokemon TCG Search application from a functional prototype into a production-grade, high-performance application. Each phase is designed to deliver measurable performance improvements while maintaining code quality and user experience.

## Implementation Status

**Current Status:** Awaiting Implementation - All phases remain unimplemented

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1: React Performance Optimization | NOT STARTED | 0% |
| Phase 2: Image Optimization | NOT STARTED | 0% |
| Phase 3: Request Optimization | NOT STARTED | 0% |
| Phase 4: Virtual Scrolling & Pagination | NOT STARTED | 0% |
| Phase 5: Code Splitting & Bundle Optimization | NOT STARTED | 0% |
| Phase 6: Performance Monitoring & Cleanup | NOT STARTED | 0% |

**Overall Progress:** 0% - No implementation has begun since this plan was created on October 31, 2025.

---

## Implementation Strategy

### Phased Approach Rationale

We'll implement improvements in **6 phases**, ordered by:
1. **ROI** (Return on Investment)
2. **User Impact** (immediate UX improvement)
3. **Technical Dependencies** (what needs to be in place first)
4. **Implementation Effort** (quick wins first)

---

## Phase 1: React Performance Optimization 🔴 CRITICAL

**Priority:** Highest
**Estimated Impact:** 40-60% reduction in re-renders
**Estimated Effort:** 4-6 hours
**Dependencies:** None
**Risk:** Low

### Goals
- Eliminate unnecessary component re-renders
- Optimize callback and computed value creation
- Improve rendering efficiency for large card lists

### Implementation Tasks

#### 1.1 Memoize All Presentational Components
**Files to Modify:**
- `src/components/CardList.tsx`
- `src/components/GridCardItem.tsx`
- `src/components/CardDisplay.tsx`
- `src/components/SearchForm.tsx`
- `src/components/LoadingSpinner.tsx`
- `src/components/ErrorMessage.tsx`

**Implementation:**
```typescript
// Before
export const CardList: React.FC<CardListProps> = ({ cards, loading, error, viewMode }) => {

// After
export const CardList = React.memo<CardListProps>(({ cards, loading, error, viewMode }) => {
  // ... component code
});
```

**Success Criteria:**
- Components only re-render when their props change
- React DevTools Profiler shows 60%+ reduction in re-renders

#### 1.2 Implement useCallback for Event Handlers
**Files to Modify:**
- `src/App.tsx` (handleFormSearch, handleSearch)
- `src/components/SearchForm.tsx` (handleSubmit)
- `src/components/GridCardItem.tsx` (onClick handlers)

**Implementation:**
```typescript
// Before
const handleFormSearch = async (query: string) => {
  // ... logic
};

// After
const handleFormSearch = useCallback(async (query: string) => {
  // ... logic
}, []); // Add dependencies as needed
```

**Success Criteria:**
- Event handlers maintain referential equality across renders
- Child components with memo don't re-render unnecessarily

#### 1.3 Implement useMemo for Computed Values
**Files to Modify:**
- `src/App.tsx` (query formatting logic)
- `src/components/CardList.tsx` (card filtering if added)

**Implementation:**
```typescript
const displayQuery = useMemo(() => {
  const queryParts = [];
  if (params.name) {
    queryParts.push(`name:*${params.name}*`);
  }
  if (params.attackName) {
    queryParts.push(`attacks.name:*${params.attackName}*`);
  }
  return queryParts.join(' AND ');
}, [params.name, params.attackName]);
```

**Success Criteria:**
- Expensive computations only run when dependencies change
- React DevTools Profiler shows computation optimization

### Testing Requirements
- Visual regression tests pass
- Component unit tests pass
- Manual testing of all user interactions
- Performance measurements using React DevTools Profiler

### Deliverables
- 6 components memoized with React.memo
- 4+ event handlers wrapped in useCallback
- 2+ computed values wrapped in useMemo
- Performance comparison report (before/after)

---

## Phase 2: Image Optimization 🔴 HIGH IMPACT

**Priority:** High
**Estimated Impact:** 2-5 second faster initial load on 3G
**Estimated Effort:** 6-8 hours
**Dependencies:** Phase 1 (for optimal re-render prevention)
**Risk:** Medium

### Goals
- Reduce initial page load time by 60%+
- Minimize bandwidth usage on mobile devices
- Improve perceived performance with progressive loading

### Implementation Tasks

#### 2.1 Implement Native Lazy Loading
**Files to Modify:**
- `src/components/GridCardItem.tsx:30-37`
- `src/components/CardDisplay.tsx:20-27`

**Implementation:**
```typescript
// Before
<img src={card.images.small} alt={card.name} />

// After
<img
  src={card.images.small}
  alt={card.name}
  loading="lazy"
  decoding="async"
/>
```

**Success Criteria:**
- Images below fold don't load until scrolled into view
- Network tab shows sequential image loading

#### 2.2 Add Intersection Observer for Advanced Lazy Loading
**New File:** `src/hooks/useLazyImage.ts`

**Implementation:**
```typescript
export function useLazyImage(src: string) {
  const [imageSrc, setImageSrc] = useState<string | undefined>(undefined);
  const [isLoaded, setIsLoaded] = useState(false);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setImageSrc(src);
            observer.disconnect();
          }
        });
      },
      { rootMargin: '50px' } // Start loading 50px before visible
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return { imgRef, imageSrc, isLoaded, setIsLoaded };
}
```

**Success Criteria:**
- Images load 50px before entering viewport
- Smooth scroll performance maintained

#### 2.3 Implement Progressive Image Loading
**New Component:** `src/components/ProgressiveImage.tsx`

**Implementation:**
```typescript
interface ProgressiveImageProps {
  lowQualitySrc: string;
  highQualitySrc: string;
  alt: string;
}

export const ProgressiveImage: React.FC<ProgressiveImageProps> = ({
  lowQualitySrc,
  highQualitySrc,
  alt
}) => {
  const [currentSrc, setCurrentSrc] = useState(lowQualitySrc);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const img = new Image();
    img.src = highQualitySrc;
    img.onload = () => {
      setCurrentSrc(highQualitySrc);
      setIsLoading(false);
    };
  }, [highQualitySrc]);

  return (
    <img
      src={currentSrc}
      alt={alt}
      style={{ filter: isLoading ? 'blur(10px)' : 'none' }}
      className={isLoading ? 'loading' : 'loaded'}
    />
  );
};
```

**Success Criteria:**
- Low-quality placeholder appears immediately
- Smooth blur-to-sharp transition
- No layout shift

#### 2.4 Add Image Error Handling and Retry
**Implementation:**
```typescript
const [retryCount, setRetryCount] = useState(0);

const handleImageError = useCallback((e: React.SyntheticEvent<HTMLImageElement>) => {
  if (retryCount < 3) {
    setTimeout(() => {
      setRetryCount(prev => prev + 1);
      e.currentTarget.src = card.images.small + '?retry=' + retryCount;
    }, 1000 * Math.pow(2, retryCount)); // Exponential backoff
  } else {
    e.currentTarget.src = '/error-blank.png';
  }
}, [retryCount, card.images.small]);
```

**Success Criteria:**
- Failed images retry with exponential backoff
- Fallback image shown after 3 failures

### Testing Requirements
- Test on throttled 3G connection
- Verify no layout shifts (CLS measurement)
- Test with browser DevTools image throttling
- Cross-browser testing (Chrome, Firefox, Safari)

### Deliverables
- Native lazy loading on all card images
- Custom hook for advanced lazy loading
- Progressive image component
- Error handling with retry logic
- Performance comparison report

---

## Phase 3: Request Optimization 🔴 HIGH IMPACT

**Priority:** High
**Estimated Impact:** 60% reduction in API calls, faster UX
**Estimated Effort:** 4-5 hours
**Dependencies:** None
**Risk:** Low

### Goals
- Eliminate duplicate API requests
- Prevent race conditions
- Improve search UX with debouncing
- Reduce API quota usage

### Implementation Tasks

#### 3.1 Implement Search Debouncing
**New Hook:** `src/hooks/useDebounce.ts`

**Implementation:**
```typescript
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

**Usage in SearchForm:**
```typescript
const [query, setQuery] = useState('');
const debouncedQuery = useDebounce(query, 300);

useEffect(() => {
  if (debouncedQuery.trim()) {
    onSearch(debouncedQuery);
  }
}, [debouncedQuery, onSearch]);
```

**Success Criteria:**
- Search only triggers 300ms after last keystroke
- No API calls during typing

#### 3.2 Implement Request Cancellation
**File to Modify:** `src/services/pokemonTcgApi.ts`

**Implementation:**
```typescript
// Create AbortController instance
let currentController: AbortController | null = null;

export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  // Cancel previous request if exists
  if (currentController) {
    currentController.abort();
  }

  // Create new controller for this request
  currentController = new AbortController();

  try {
    const response = await axiosInstance.get<ApiResponse>('/cards', {
      params: requestParams,
      signal: currentController.signal
    });

    currentController = null;
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request cancelled');
      throw new Error('Request cancelled');
    }
    throw error;
  }
}
```

**Success Criteria:**
- Rapid successive searches cancel previous requests
- No race conditions in result display

#### 3.3 Implement LRU Cache for Search Results
**New File:** `src/utils/cache.ts`

**Implementation:**
```typescript
class LRUCache<K, V> {
  private cache: Map<K, V>;
  private maxSize: number;

  constructor(maxSize: number = 50) {
    this.cache = new Map();
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
    // Remove oldest if at capacity
    if (this.cache.size >= this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  has(key: K): boolean {
    return this.cache.has(key);
  }

  clear(): void {
    this.cache.clear();
  }
}

export const searchCache = new LRUCache<string, ApiResponse>(50);
```

**Usage in API:**
```typescript
export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  const cacheKey = JSON.stringify(params);

  // Check cache first
  if (searchCache.has(cacheKey)) {
    console.log('[CACHE HIT] Returning cached results');
    return searchCache.get(cacheKey)!;
  }

  // ... make API request ...

  // Cache the response
  searchCache.set(cacheKey, response.data);
  return response.data;
}
```

**Success Criteria:**
- Duplicate searches return instantly from cache
- Cache size limited to 50 entries (LRU eviction)
- Cache hit rate > 30% in typical usage

#### 3.4 Fix Timer Cleanup
**File to Modify:** `src/App.tsx:55-63`

**Current Issue (Verified November 1, 2025):**
- Timer interval is currently created inside `handleSearch` function (line 55)
- Timer is scoped to the function, making cleanup difficult
- Timer may not properly clean up if component unmounts during search

**Implementation:**
```typescript
useEffect(() => {
  let timerInterval: NodeJS.Timeout | null = null;

  if (loading) {
    timerInterval = setInterval(() => {
      setTimeRemaining(prev => {
        if (prev <= 1) {
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  }

  return () => {
    if (timerInterval) {
      clearInterval(timerInterval);
    }
  };
}, [loading]);
```

**Success Criteria:**
- Timer moved to useEffect with proper dependency on `loading` state
- No memory leaks in React DevTools
- Timer stops immediately when component unmounts or loading state changes

### Testing Requirements
- Test rapid search typing
- Test back-button navigation
- Monitor network tab for cancelled requests
- Verify cache hit rate in console
- Memory leak testing with React DevTools

### Deliverables
- Debouncing hook implemented
- AbortController request cancellation
- LRU cache with 50-entry limit
- Fixed timer cleanup
- Request optimization metrics

---

## Phase 4: Virtual Scrolling & Pagination 🟡 MEDIUM-HIGH IMPACT

**Priority:** Medium-High
**Estimated Impact:** 50%+ faster rendering with 100+ cards
**Estimated Effort:** 8-10 hours
**Dependencies:** Phase 1
**Risk:** Medium-High

### Goals
- Handle 250+ card results smoothly
- Reduce memory footprint
- Improve scroll performance

### Implementation Tasks

#### 4.1 Implement Pagination UI
**File to Modify:** `src/components/CardList.tsx`

**Implementation:**
```typescript
interface CardListProps {
  cards: PokemonCard[];
  loading: boolean;
  error: string | null;
  viewMode: 'card-view' | 'detailed-view';
  totalCount: number;
  currentPage: number;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
}

// Add pagination controls
<div className="pagination-controls">
  <button
    onClick={() => onPageChange(currentPage - 1)}
    disabled={currentPage === 1}
  >
    Previous
  </button>

  <span>Page {currentPage} of {Math.ceil(totalCount / pageSize)}</span>

  <button
    onClick={() => onPageChange(currentPage + 1)}
    disabled={currentPage * pageSize >= totalCount}
  >
    Next
  </button>

  <select onChange={(e) => onPageSizeChange(Number(e.target.value))}>
    <option value="20">20 per page</option>
    <option value="50">50 per page</option>
    <option value="100">100 per page</option>
  </select>
</div>
```

**Success Criteria:**
- Users can navigate pages
- Page size selector works
- URL reflects current page (if routing added)

#### 4.2 Implement Virtual Scrolling (react-window)
**New Dependency:** `npm install react-window @types/react-window`

**New Component:** `src/components/VirtualCardGrid.tsx`

**Implementation:**
```typescript
import { FixedSizeGrid } from 'react-window';

interface VirtualCardGridProps {
  cards: PokemonCard[];
  columnCount: number;
  cardWidth: number;
  cardHeight: number;
}

export const VirtualCardGrid: React.FC<VirtualCardGridProps> = ({
  cards,
  columnCount,
  cardWidth,
  cardHeight
}) => {
  const Cell = ({ columnIndex, rowIndex, style }: any) => {
    const index = rowIndex * columnCount + columnIndex;
    if (index >= cards.length) return null;

    return (
      <div style={style}>
        <GridCardItem card={cards[index]} />
      </div>
    );
  };

  return (
    <FixedSizeGrid
      columnCount={columnCount}
      columnWidth={cardWidth}
      height={window.innerHeight - 200}
      rowCount={Math.ceil(cards.length / columnCount)}
      rowHeight={cardHeight}
      width={window.innerWidth - 40}
    >
      {Cell}
    </FixedSizeGrid>
  );
};
```

**Success Criteria:**
- Only visible cards rendered in DOM
- Smooth 60fps scrolling with 100+ cards
- Memory usage stays constant regardless of card count

#### 4.3 Implement Infinite Scroll (Alternative to Pagination)
**New Hook:** `src/hooks/useInfiniteScroll.ts`

**Implementation:**
```typescript
export function useInfiniteScroll(callback: () => void, hasMore: boolean) {
  const loaderRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMore) {
          callback();
        }
      },
      { threshold: 1.0 }
    );

    if (loaderRef.current) {
      observer.observe(loaderRef.current);
    }

    return () => observer.disconnect();
  }, [callback, hasMore]);

  return loaderRef;
}
```

**Success Criteria:**
- New cards load automatically when scrolling to bottom
- Loading indicator appears during fetch
- Smooth scroll maintained

### Testing Requirements
- Test with 250 cards (API maximum)
- Scroll performance testing (Chrome DevTools Performance)
- Memory profiling with 250+ cards
- Mobile device testing

### Deliverables
- Pagination UI with page controls
- Virtual scrolling with react-window
- Infinite scroll hook (alternative)
- Performance comparison (virtualized vs non-virtualized)

---

## Phase 5: Code Splitting & Bundle Optimization 🟡 MEDIUM IMPACT

**Priority:** Medium
**Estimated Impact:** 20-30% smaller initial bundle
**Estimated Effort:** 3-4 hours
**Dependencies:** None
**Risk:** Low

### Goals
- Reduce initial bundle size
- Improve Time to Interactive (TTI)
- Enable faster page loads

### Implementation Tasks

#### 5.1 Lazy Load CardDisplay Component
**File to Modify:** `src/components/GridCardItem.tsx`

**Implementation:**
```typescript
import { lazy, Suspense } from 'react';

const CardDisplay = lazy(() => import('./CardDisplay'));

export const GridCardItem: React.FC<GridCardItemProps> = ({ card }) => {
  const [showDetails, setShowDetails] = useState(false);

  if (showDetails) {
    return (
      <div className="card-grid-item-expanded">
        <Suspense fallback={<LoadingSpinner />}>
          <CardDisplay card={card} />
        </Suspense>
      </div>
    );
  }
  // ...
};
```

**Success Criteria:**
- CardDisplay only loads when user clicks a card
- Network tab shows separate chunk loaded on demand

#### 5.2 Remove Unused Components
**Files Status (Verified November 1, 2025):**
- `src/components/ResultsList.tsx` - Used in tests (`src/tests/components.test.tsx`)
- `src/components/CardItem.tsx` - Used by `ResultsList.tsx` and in tests
- `src/components/SkeletonLoader.tsx` - Used in tests only, not imported in App
- `src/components/DebugLogs.tsx` - Not imported anywhere (safe to remove)
- `src/components/SearchForm+Attack.tsx` - Not imported anywhere (safe to remove)

**Files to Delete:**
- `src/components/DebugLogs.tsx`
- `src/components/SearchForm+Attack.tsx`

**Files Requiring Test Updates:**
- `src/components/ResultsList.tsx` - Remove from tests or refactor tests
- `src/components/CardItem.tsx` - Remove from tests or refactor tests
- `src/components/SkeletonLoader.tsx` - Remove from tests or refactor tests

**Testing Required:**
- Update or remove tests that reference `ResultsList`, `CardItem`, `SkeletonLoader`
- Ensure no imports reference deleted files
- Run build and verify bundle size reduction

**Success Criteria:**
- Bundle size reduced by 10-15KB (after test refactoring)
- All tests still pass

#### 5.3 Strip Console Logs in Production
**File to Modify:** `vite.config.ts`

**Current Status (Verified November 1, 2025):**
- 14+ console.log/warn statements found in:
  - `App.tsx:52` - 1 instance
  - `pokemonTcgApi.ts:45-78` - 12 instances
  - `src/utils/logger.ts:89` - 1 instance (centralized logging utility exists but unused)

**Note:** A centralized logging utility exists at `src/utils/logger.ts` that could be used to consolidate all logging statements before implementing production stripping.

**Implementation:**
```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    strictPort: false,
  },
  build: {
    rollupOptions: {
      plugins: [
        {
          name: 'strip-console',
          transform(code, id) {
            if (id.includes('node_modules')) return null;
            return code.replace(/console\.(log|debug|info|warn)\([^)]*\);?/g, '');
          }
        }
      ]
    }
  }
});
```

**Success Criteria:**
- No console.log statements in production build
- console.error still works for critical errors
- Consider consolidating to `logger.ts` utility before stripping

#### 5.4 Consolidate CSS Files
**Goal:** Merge duplicate App.css files (if any exist)

**Files Status (Verified November 1, 2025):**
- `src/styles/App.css` - Exists and used in App.tsx
- No duplicate `src/App.css` found at root level
- Multiple CSS files exist but are properly scoped:
  - `src/styles/App.css`
  - `src/components/GridCardItem.css`
  - `src/components/LoadingSpinner.css`
  - `src/components/ErrorMessage.css`
  - `index.css`

**Files to Consider:**
- Verify if CSS can be consolidated or if current structure is optimal
- Consider critical CSS extraction for faster initial render

**Success Criteria:**
- Optimized CSS loading strategy
- No style regressions
- Improved initial render performance

### Testing Requirements
- Build production bundle
- Verify bundle analysis with rollup-plugin-visualizer
- Test lazy loading in production build
- Visual regression testing

### Deliverables
- Lazy loaded CardDisplay
- 5 unused components removed
- Console logs stripped in production
- CSS files consolidated
- Bundle size report

---

## Phase 6: Performance Monitoring & Cleanup 🟡 MEDIUM IMPACT

**Priority:** Medium
**Estimated Impact:** Enables ongoing optimization
**Estimated Effort:** 4-5 hours
**Dependencies:** All previous phases
**Risk:** Low

### Goals
- Establish performance baseline
- Enable continuous monitoring
- Set performance budgets

### Implementation Tasks

#### 6.1 Implement Performance Metrics
**New File:** `src/utils/metrics.ts`

**Implementation:**
```typescript
export class PerformanceMetrics {
  static markStart(name: string): void {
    performance.mark(`${name}-start`);
  }

  static markEnd(name: string): void {
    performance.mark(`${name}-end`);
    performance.measure(name, `${name}-start`, `${name}-end`);

    const measure = performance.getEntriesByName(name)[0];
    console.log(`[PERF] ${name}: ${measure.duration.toFixed(2)}ms`);
  }

  static async measureApiCall<T>(
    name: string,
    apiCall: () => Promise<T>
  ): Promise<T> {
    this.markStart(name);
    try {
      const result = await apiCall();
      this.markEnd(name);
      return result;
    } catch (error) {
      this.markEnd(name);
      throw error;
    }
  }
}
```

**Usage:**
```typescript
// Measure API calls
const response = await PerformanceMetrics.measureApiCall(
  'search-cards',
  () => searchCards(params)
);

// Measure render time
PerformanceMetrics.markStart('card-list-render');
// ... render logic ...
PerformanceMetrics.markEnd('card-list-render');
```

**Success Criteria:**
- Key metrics logged to console
- Performance entries available in DevTools

#### 6.2 Implement Error Rate Tracking
**New File:** `src/utils/errorTracking.ts`

**Implementation:**
```typescript
class ErrorTracker {
  private errors: Map<string, number> = new Map();

  track(errorType: string): void {
    const count = this.errors.get(errorType) || 0;
    this.errors.set(errorType, count + 1);
  }

  getErrorRate(errorType: string): number {
    return this.errors.get(errorType) || 0;
  }

  getAllErrors(): Record<string, number> {
    return Object.fromEntries(this.errors);
  }

  reset(): void {
    this.errors.clear();
  }
}

export const errorTracker = new ErrorTracker();
```

**Success Criteria:**
- Error rates tracked per type
- Dashboard shows error frequency

#### 6.3 Set Performance Budgets
**New File:** `performance-budget.json`

**Implementation:**
```json
{
  "budgets": [
    {
      "resourceSizes": [
        {
          "resourceType": "script",
          "budget": 200
        },
        {
          "resourceType": "stylesheet",
          "budget": 20
        },
        {
          "resourceType": "image",
          "budget": 500
        }
      ],
      "timings": [
        {
          "metric": "interactive",
          "budget": 3000
        },
        {
          "metric": "first-contentful-paint",
          "budget": 1500
        }
      ]
    }
  ]
}
```

**Vite Configuration:**
```typescript
export default defineConfig({
  build: {
    reportCompressedSize: true,
    chunkSizeWarningLimit: 200
  }
});
```

**Success Criteria:**
- Build warns if budgets exceeded
- CI fails on budget violations

#### 6.4 Add Web Vitals Monitoring
**New Dependency:** `npm install web-vitals`

**File to Modify:** `src/main.tsx`

**Implementation:**
```typescript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function sendToAnalytics({ name, value, id }: any) {
  console.log(`[Web Vital] ${name}: ${value} (${id})`);
  // In production, send to analytics service
}

getCLS(sendToAnalytics);
getFID(sendToAnalytics);
getFCP(sendToAnalytics);
getLCP(sendToAnalytics);
getTTFB(sendToAnalytics);
```

**Success Criteria:**
- Core Web Vitals tracked
- Metrics logged to console (dev) / analytics (prod)

### Testing Requirements
- Run Lighthouse audits before and after
- Verify metrics accuracy
- Test error tracking with simulated errors

### Deliverables
- Performance metrics utility
- Error rate tracking
- Performance budgets defined
- Web Vitals monitoring
- Lighthouse audit report

---

## Success Metrics

### Performance Targets

| Metric | Current | Target | Method |
|--------|---------|--------|--------|
| Initial Bundle Size | 192KB | <150KB | Code splitting |
| Time to Interactive | ~2.5s | <2s | All optimizations |
| First Contentful Paint | ~1.2s | <1s | Image optimization |
| Cumulative Layout Shift | Unknown | <0.1 | Image sizing |
| Total Blocking Time | Unknown | <200ms | React optimization |
| Re-render Count | High | -60% | Memoization |
| API Cache Hit Rate | 0% | >30% | LRU cache |

### Quality Targets

- Zero console.log statements in production
- Zero unused components
- 100% test coverage maintained
- Zero accessibility regressions
- Zero visual regressions

---

## Risk Mitigation

### Phase 1 Risks
- **Risk:** Breaking existing functionality with memoization
- **Mitigation:** Extensive testing, gradual rollout, A/B testing

### Phase 2 Risks
- **Risk:** Image lazy loading causing layout shifts
- **Mitigation:** Explicit width/height attributes, aspect ratio boxes

### Phase 3 Risks
- **Risk:** Cache invalidation bugs
- **Mitigation:** Clear cache on app update, size limits, TTL

### Phase 4 Risks
- **Risk:** Virtual scrolling complexity
- **Mitigation:** Thorough testing, fallback to standard rendering

---

## Timeline Estimate

| Phase | Duration | Dependencies | Start After |
|-------|----------|--------------|-------------|
| Phase 1 | 4-6 hours | None | Immediate |
| Phase 2 | 6-8 hours | Phase 1 | Day 1 |
| Phase 3 | 4-5 hours | None | Day 1 |
| Phase 4 | 8-10 hours | Phase 1 | Day 2 |
| Phase 5 | 3-4 hours | None | Day 3 |
| Phase 6 | 4-5 hours | All phases | Day 3 |

**Total Estimated Effort:** 29-38 hours (4-5 days)

---

## Rollout Strategy

### Development Branch
- Implement each phase in feature branch
- Merge to performance-audit branch
- Run full test suite

### Testing
- Unit tests for all new utilities
- Integration tests for performance features
- E2E tests for critical user paths
- Visual regression testing

### Staging
- Deploy to staging environment
- Run Lighthouse audits
- Gather performance metrics
- User acceptance testing

### Production
- Gradual rollout (10% → 50% → 100%)
- Monitor error rates
- Track performance metrics
- Rollback plan ready

---

## Measurement & Validation

### Before Implementation
- Run Lighthouse audit (current baseline)
- Measure bundle size (192KB)
- Count re-renders with React DevTools
- Measure API response times
- Document current load times

### After Each Phase
- Run Lighthouse audit
- Compare bundle sizes
- Measure re-render reduction
- Calculate cache hit rate
- Document improvements

### Final Validation
- Side-by-side comparison
- Performance improvement report
- User feedback collection
- Load testing results

---

## Maintenance Plan

### Ongoing Monitoring
- Weekly Lighthouse audits
- Monthly performance reviews
- Bundle size tracking
- Error rate monitoring

### Performance Budget Enforcement
- CI/CD checks for bundle size
- Automated Lighthouse in CI
- Pre-commit hooks for console.log detection

### Documentation
- Update README with performance features
- Document caching strategy
- Maintain performance runbook

---

## Conclusion

This phased approach ensures:
1. **Quick Wins:** High ROI improvements first
2. **Low Risk:** Gradual, testable changes
3. **Measurable:** Clear metrics at each phase
4. **Maintainable:** Sustainable performance culture

**Expected Final Outcome:**
- 40-60% fewer re-renders
- 2-5 second faster initial load
- <150KB initial bundle
- 60% fewer API calls
- Production-ready performance monitoring

---

**Plan Created:** October 31, 2025
**Last Updated:** November 1, 2025
**Plan Owner:** Claude Performance Optimization Agent
**Status:** Awaiting Implementation - All phases remain unimplemented
**Next Step:** Begin Phase 1 Implementation when ready
