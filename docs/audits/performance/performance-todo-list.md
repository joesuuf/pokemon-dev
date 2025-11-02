# Performance Audit - Action Items & To-Do List

**Date:** November 1, 2025  
**Audit Version:** 2.0  
**Overall Score:** 72/100 ??

---

## ?? Critical Priority (Fix Immediately)

### Issue #1: React Component Memoization
**Severity:** ?? Critical  
**Impact:** 40-60% reduction in unnecessary re-renders  
**Estimated Effort:** 4-6 hours  
**ROI:** ?????

#### To-Do List:

- [ ] **Task 1.1:** Memoize CardList Component
  - [ ] Open `src/components/CardList.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Verify props interface is properly typed
  - [ ] Test component still works correctly

- [ ] **Task 1.2:** Memoize GridCardItem Component
  - [ ] Open `src/components/GridCardItem.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Test card rendering still works
  - [ ] Test card click interactions

- [ ] **Task 1.3:** Memoize CardDisplay Component
  - [ ] Open `src/components/CardDisplay.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Test detailed card view still works

- [ ] **Task 1.4:** Memoize SearchForm Component
  - [ ] Open `src/components/SearchForm.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Test form submission still works

- [ ] **Task 1.5:** Memoize LoadingSpinner Component
  - [ ] Open `src/components/LoadingSpinner.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Test loading state display

- [ ] **Task 1.6:** Memoize ErrorMessage Component
  - [ ] Open `src/components/ErrorMessage.tsx`
  - [ ] Import `React.memo` from 'react'
  - [ ] Wrap component export with `React.memo`
  - [ ] Test error display still works

- [ ] **Task 1.7:** Test Memoization Impact
  - [ ] Open React DevTools Profiler
  - [ ] Record render performance before changes
  - [ ] Apply memoization changes
  - [ ] Record render performance after changes
  - [ ] Compare re-render counts
  - [ ] Document improvement percentage

- [ ] **Task 1.8:** Commit Changes
  - [ ] Stage all modified component files
  - [ ] Commit with message: "perf: add React.memo to all presentational components"

**Code Reference:**
```typescript
// BEFORE
export const CardList: React.FC<CardListProps> = ({ cards, loading, error, viewMode }) => {
  // Component code
};

// AFTER
export const CardList = React.memo<CardListProps>(({ cards, loading, error, viewMode }) => {
  // Component code
});
```

---

### Issue #2: Callback Memoization with useCallback
**Severity:** ?? Critical  
**Impact:** Prevents unnecessary re-renders, enables memoization benefits  
**Estimated Effort:** 1-2 hours  
**ROI:** ?????

#### To-Do List:

- [ ] **Task 2.1:** Memoize handleFormSearch callback
  - [ ] Open `src/App.tsx`
  - [ ] Import `useCallback` from 'react'
  - [ ] Wrap `handleFormSearch` with `useCallback`
  - [ ] Add dependencies: `[]` (empty if no dependencies)
  - [ ] Verify function still works

- [ ] **Task 2.2:** Memoize handleSearch callback
  - [ ] In `src/App.tsx`
  - [ ] Wrap `handleSearch` with `useCallback`
  - [ ] Add dependencies: `[setLoading, setError, setTimeRemaining, setCards, setSearchQuery]`
  - [ ] Verify search functionality still works

- [ ] **Task 2.3:** Memoize GridCardItem callbacks
  - [ ] Open `src/components/GridCardItem.tsx`
  - [ ] Import `useCallback` from 'react'
  - [ ] Wrap `setShowDetails` callbacks with `useCallback`
  - [ ] Test card click interactions

- [ ] **Task 2.4:** Test Callback Memoization
  - [ ] Use React DevTools Profiler
  - [ ] Verify components don't re-render unnecessarily
  - [ ] Test all user interactions still work

- [ ] **Task 2.5:** Commit Changes
  - [ ] Stage modified files
  - [ ] Commit with message: "perf: add useCallback to event handlers"

**Code Reference:**
```typescript
// BEFORE
const handleFormSearch = async (query: string) => {
  const params: SearchParams = { name: query };
  await handleSearch(params);
};

// AFTER
const handleFormSearch = useCallback(async (query: string) => {
  const params: SearchParams = { name: query };
  await handleSearch(params);
}, [handleSearch]);
```

---

### Issue #3: Computed Value Memoization with useMemo
**Severity:** ?? Medium (but quick win)  
**Impact:** Prevents redundant calculations  
**Estimated Effort:** 1 hour  
**ROI:** ????

#### To-Do List:

- [ ] **Task 3.1:** Memoize Query Formatting Logic
  - [ ] Open `src/App.tsx`
  - [ ] Import `useMemo` from 'react'
  - [ ] Find query formatting logic (around line 42-58)
  - [ ] Extract to `useMemo` hook
  - [ ] Add dependencies: `[params.name, params.attackName]`

- [ ] **Task 3.2:** Memoize Card Filtering/Mapping (if any)
  - [ ] Check `src/components/CardList.tsx`
  - [ ] If card filtering exists, wrap in `useMemo`
  - [ ] Add appropriate dependencies

- [ ] **Task 3.3:** Test Memoization
  - [ ] Verify queries format correctly
  - [ ] Check React DevTools for computation optimization
  - [ ] Test search functionality

- [ ] **Task 3.4:** Commit Changes
  - [ ] Stage modified files
  - [ ] Commit with message: "perf: add useMemo for expensive computations"

**Code Reference:**
```typescript
// BEFORE
const displayQuery = queryParts.join(' AND ');

// AFTER
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

---

### Issue #4: Timer Cleanup (Same as Security Issue #1)
**Severity:** ?? Critical  
**Impact:** Memory leak prevention  
**Estimated Effort:** 1 hour  
**See:** `docs/audits/security/security-todo-list.md` Issue #1

---

## ?? High Priority (Fix Within Sprint)

### Issue #5: Request Cancellation with AbortController
**Severity:** ?? High  
**Impact:** Prevents race conditions, improves UX  
**Estimated Effort:** 2 hours  
**ROI:** ????

#### To-Do List:

- [ ] **Task 5.1:** Create AbortController Instance
  - [ ] Open `src/services/pokemonTcgApi.ts`
  - [ ] Create module-level variable: `let currentController: AbortController | null = null;`
  - [ ] Initialize at top of file

- [ ] **Task 5.2:** Implement Request Cancellation
  - [ ] In `searchCards` function
  - [ ] Check if `currentController` exists
  - [ ] If exists, call `currentController.abort()`
  - [ ] Create new `AbortController()` instance
  - [ ] Assign to `currentController`

- [ ] **Task 5.3:** Add Signal to Axios Request
  - [ ] In `axiosInstance.get()` call
  - [ ] Add `signal: currentController.signal` to request config
  - [ ] Import `AxiosError` type if needed

- [ ] **Task 5.4:** Handle Cancellation Errors
  - [ ] In catch block
  - [ ] Check if error is `axios.isCancel(error)`
  - [ ] If cancelled, throw appropriate error or return empty result
  - [ ] Otherwise, throw original error

- [ ] **Task 5.5:** Clear Controller After Success
  - [ ] After successful response
  - [ ] Set `currentController = null`

- [ ] **Task 5.6:** Test Request Cancellation
  - [ ] Start search for "Pikachu"
  - [ ] Immediately start search for "Charizard"
  - [ ] Verify only "Charizard" results appear
  - [ ] Check network tab for cancelled requests
  - [ ] Verify no race conditions

- [ ] **Task 5.7:** Commit Changes
  - [ ] Stage `src/services/pokemonTcgApi.ts`
  - [ ] Commit with message: "perf: add request cancellation to prevent race conditions"

**Code Reference:**
```typescript
let currentController: AbortController | null = null;

export async function searchCards(params: SearchParams): Promise<ApiResponse> {
  if (currentController) {
    currentController.abort();
  }
  
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
      throw new Error('Request cancelled');
    }
    throw error;
  }
}
```

---

### Issue #6: Request Caching with LRU Cache
**Severity:** ?? High  
**Impact:** 60%+ reduction in API calls, faster UX  
**Estimated Effort:** 3-4 hours  
**ROI:** ?????

#### To-Do List:

- [ ] **Task 6.1:** Create LRU Cache Utility
  - [ ] Create new file: `src/utils/cache.ts`
  - [ ] Implement LRU Cache class:
    - [ ] Private `cache: Map<K, V>`
    - [ ] Private `maxSize: number`
    - [ ] Constructor with `maxSize` parameter (default: 50)
    - [ ] `get(key: K): V | undefined` method
    - [ ] `set(key: K, value: V): void` method
    - [ ] `has(key: K): boolean` method
    - [ ] `clear(): void` method
  - [ ] Implement LRU eviction logic

- [ ] **Task 6.2:** Create Cache Instance for Search Results
  - [ ] In `src/utils/cache.ts`
  - [ ] Export `searchCache` instance: `new LRUCache<string, ApiResponse>(50)`
  - [ ] Import `ApiResponse` type

- [ ] **Task 6.3:** Integrate Cache into API Service
  - [ ] Open `src/services/pokemonTcgApi.ts`
  - [ ] Import `searchCache` from `../utils/cache`
  - [ ] In `searchCards` function
  - [ ] Create cache key: `JSON.stringify(params)`
  - [ ] Check cache: `if (searchCache.has(cacheKey))`
  - [ ] Return cached result if exists
  - [ ] After API call, cache result: `searchCache.set(cacheKey, response.data)`

- [ ] **Task 6.4:** Add Cache Hit Logging (Optional)
  - [ ] Log cache hits for debugging
  - [ ] Use logger utility (not console.log)

- [ ] **Task 6.5:** Test Caching
  - [ ] Search for "Pikachu"
  - [ ] Verify API call made
  - [ ] Search for "Pikachu" again
  - [ ] Verify no API call (cache hit)
  - [ ] Verify results appear instantly
  - [ ] Test with different search params
  - [ ] Test cache eviction (50+ entries)

- [ ] **Task 6.6:** Add Cache Statistics (Optional)
  - [ ] Track cache hits/misses
  - [ ] Log cache statistics
  - [ ] Display cache hit rate

- [ ] **Task 6.7:** Commit Changes
  - [ ] Stage `src/utils/cache.ts` and `src/services/pokemonTcgApi.ts`
  - [ ] Commit with message: "perf: implement LRU cache for search results"

**Code Reference:**
```typescript
// src/utils/cache.ts
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
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
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

---

### Issue #7: Request Debouncing
**Severity:** ?? High  
**Impact:** Prevents rapid-fire API calls, better UX  
**Estimated Effort:** 1-2 hours  
**ROI:** ????

#### To-Do List:

- [ ] **Task 7.1:** Create useDebounce Hook
  - [ ] Create new file: `src/hooks/useDebounce.ts`
  - [ ] Implement hook:
    - [ ] Accept `value: T` and `delay: number` parameters
    - [ ] Use `useState` for `debouncedValue`
    - [ ] Use `useEffect` with timeout
    - [ ] Return `debouncedValue`
    - [ ] Cleanup timeout on unmount or value change

- [ ] **Task 7.2:** Integrate Debouncing into SearchForm (Optional)
  - [ ] Open `src/components/SearchForm.tsx`
  - [ ] Import `useDebounce` hook
  - [ ] Add local state for search input
  - [ ] Debounce input value (300ms delay)
  - [ ] Call `onSearch` with debounced value

- [ ] **Task 7.3:** Test Debouncing
  - [ ] Type rapidly in search input
  - [ ] Verify API call only triggers after 300ms pause
  - [ ] Check network tab for request count
  - [ ] Verify no unnecessary API calls

- [ ] **Task 7.4:** Commit Changes
  - [ ] Stage `src/hooks/useDebounce.ts` and `src/components/SearchForm.tsx`
  - [ ] Commit with message: "perf: add request debouncing to prevent rapid API calls"

**Code Reference:**
```typescript
// src/hooks/useDebounce.ts
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

---

## ?? Medium Priority (Backlog)

### Issue #8: Lazy Load CardDisplay Component
**Severity:** ?? Medium  
**Impact:** Smaller initial bundle, faster load  
**Estimated Effort:** 1 hour

#### To-Do List:

- [ ] **Task 8.1:** Lazy Load CardDisplay
  - [ ] Open `src/components/GridCardItem.tsx`
  - [ ] Import `lazy` and `Suspense` from 'react'
  - [ ] Change CardDisplay import to lazy load
  - [ ] Wrap CardDisplay in Suspense boundary
  - [ ] Add loading fallback

- [ ] **Task 8.2:** Test Lazy Loading
  - [ ] Verify CardDisplay loads on demand
  - [ ] Check network tab for separate chunk
  - [ ] Test loading state

- [ ] **Task 8.3:** Commit Changes
  - [ ] Stage `src/components/GridCardItem.tsx`
  - [ ] Commit with message: "perf: lazy load CardDisplay component"

---

### Issue #9: Progressive Image Loading
**Severity:** ?? Medium  
**Impact:** Better perceived performance  
**Estimated Effort:** 3-4 hours

#### To-Do List:

- [ ] **Task 9.1:** Create ProgressiveImage Component
  - [ ] Create `src/components/ProgressiveImage.tsx`
  - [ ] Implement blur-up placeholder strategy
  - [ ] Handle low-quality ? high-quality transition
  - [ ] Add loading state management

- [ ] **Task 9.2:** Integrate ProgressiveImage
  - [ ] Replace `<img>` tags in `GridCardItem.tsx`
  - [ ] Replace `<img>` tags in `CardDisplay.tsx`
  - [ ] Use Pokemon TCG API image variants

- [ ] **Task 9.3:** Test Progressive Loading
  - [ ] Test on slow network
  - [ ] Verify blur-up effect
  - [ ] Check layout shift (CLS)

- [ ] **Task 9.4:** Commit Changes
  - [ ] Stage new and modified files
  - [ ] Commit with message: "perf: implement progressive image loading"

---

### Issue #10: Virtual Scrolling
**Severity:** ?? Medium  
**Impact:** Handle 250+ cards smoothly  
**Estimated Effort:** 8-10 hours

#### To-Do List:

- [ ] **Task 10.1:** Install react-window
  - [ ] Run `npm install react-window @types/react-window`
  - [ ] Verify installation

- [ ] **Task 10.2:** Create VirtualCardGrid Component
  - [ ] Create `src/components/VirtualCardGrid.tsx`
  - [ ] Implement FixedSizeGrid from react-window
  - [ ] Configure grid dimensions
  - [ ] Handle cell rendering

- [ ] **Task 10.3:** Integrate Virtual Scrolling
  - [ ] Update `CardList.tsx` to use VirtualCardGrid
  - [ ] Configure column count
  - [ ] Set card dimensions

- [ ] **Task 10.4:** Test Virtual Scrolling
  - [ ] Test with 250 cards
  - [ ] Verify smooth scrolling
  - [ ] Check DOM node count
  - [ ] Measure memory usage

- [ ] **Task 10.5:** Commit Changes
  - [ ] Stage all modified files
  - [ ] Commit with message: "perf: implement virtual scrolling for large card lists"

---

### Issue #11: Performance Monitoring
**Severity:** ?? Medium  
**Impact:** Ongoing optimization insights  
**Estimated Effort:** 4-5 hours

#### To-Do List:

- [ ] **Task 11.1:** Install web-vitals
  - [ ] Run `npm install web-vitals`
  - [ ] Verify installation

- [ ] **Task 11.2:** Create Performance Metrics Utility
  - [ ] Create `src/utils/metrics.ts`
  - [ ] Implement PerformanceMetrics class
  - [ ] Add markStart/markEnd methods
  - [ ] Add measureApiCall method

- [ ] **Task 11.3:** Integrate Web Vitals
  - [ ] Open `src/main.tsx`
  - [ ] Import web-vitals functions
  - [ ] Set up Core Web Vitals tracking
  - [ ] Configure analytics reporting

- [ ] **Task 11.4:** Add Performance Budgets
  - [ ] Create `performance-budget.json`
  - [ ] Set bundle size limits
  - [ ] Set timing budgets
  - [ ] Configure in Vite

- [ ] **Task 11.5:** Test Performance Monitoring
  - [ ] Verify metrics logged
  - [ ] Check Performance API entries
  - [ ] Test Web Vitals collection

- [ ] **Task 11.6:** Commit Changes
  - [ ] Stage all modified files
  - [ ] Commit with message: "perf: add performance monitoring and Web Vitals tracking"

---

## Summary Checklist

### Critical (Fix Immediately)
- [ ] Issue #1: React Component Memoization
- [ ] Issue #2: Callback Memoization
- [ ] Issue #3: Computed Value Memoization
- [ ] Issue #4: Timer Cleanup

### High Priority (Within Sprint)
- [ ] Issue #5: Request Cancellation
- [ ] Issue #6: Request Caching
- [ ] Issue #7: Request Debouncing

### Medium Priority (Backlog)
- [ ] Issue #8: Lazy Load CardDisplay
- [ ] Issue #9: Progressive Image Loading
- [ ] Issue #10: Virtual Scrolling
- [ ] Issue #11: Performance Monitoring

---

## Testing Checklist

After completing each issue:
- [ ] Run `npm run build` - verify build succeeds
- [ ] Run `npm test` - verify tests pass
- [ ] Test functionality manually
- [ ] Check React DevTools Profiler for improvements
- [ ] Measure performance metrics (if monitoring implemented)

---

**Last Updated:** November 1, 2025  
**Next Review:** After each issue completion
