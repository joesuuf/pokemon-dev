/**
 * Masterlist Service for Static Site
 * Caches cards locally for faster searches
 */

'use strict';

const MasterlistService = (function() {
    let masterlistCache = null;
    let isLoadingMasterlist = false;
    let loadPromise = null;

    /**
     * Load masterlist from API
     */
    async function loadMasterlist() {
        if (loadPromise) {
            return loadPromise;
        }

        if (masterlistCache) {
            return masterlistCache;
        }

        if (isLoadingMasterlist) {
            return loadPromise;
        }

        isLoadingMasterlist = true;

        loadPromise = (async () => {
            try {
                console.log('[MASTERLIST] Loading Pokemon card masterlist...');
                
                const query = encodeURIComponent('name:*');
                const pageSize = 1000;
                const apiUrl = 'https://api.pokemontcg.io/v2/cards';
                
                const url = `${apiUrl}?q=${query}&pageSize=${pageSize}&orderBy=name`;
                console.log('[MASTERLIST] Fetching from:', url);

                const response = await fetch(url, {
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error(`Failed to load masterlist: ${response.status} ${response.statusText}`);
                }

                const data = await response.json();
                const allCards = data.data;

                console.log(`[MASTERLIST] Loaded ${allCards.length} cards (total available: ${data.totalCount})`);
                
                masterlistCache = allCards;
                console.log(`[MASTERLIST] Masterlist loaded successfully: ${allCards.length} cards`);
                
                return allCards;
            } catch (error) {
                console.error('[MASTERLIST] Error loading masterlist:', error);
                isLoadingMasterlist = false;
                loadPromise = null;
                throw error;
            } finally {
                isLoadingMasterlist = false;
            }
        })();

        return loadPromise;
    }

    /**
     * Search through masterlist
     */
    function searchMasterlist(cards, query) {
        let results = cards;
        const queryLower = query.toLowerCase().trim();

        if (queryLower) {
            results = results.filter(card => {
                const cardNameLower = card.name.toLowerCase();
                return cardNameLower.includes(queryLower);
            });
        }

        // Sort by name
        results = results.sort((a, b) => {
            const nameCompare = a.name.localeCompare(b.name);
            if (nameCompare !== 0) return nameCompare;
            return parseInt(b.number) - parseInt(a.number);
        });

        return results;
    }

    /**
     * Search cards using masterlist
     */
    async function searchCards(query, page = 1, pageSize = 20) {
        try {
            console.log('[MASTERLIST] Searching masterlist for:', query);

            const masterlist = await loadMasterlist();
            let results = searchMasterlist(masterlist, query);

            const totalCount = results.length;
            const startIndex = (page - 1) * pageSize;
            const endIndex = startIndex + pageSize;
            const paginatedResults = results.slice(startIndex, endIndex);

            console.log(`[MASTERLIST] Found ${totalCount} total matches, returning page ${page} (${paginatedResults.length} cards)`);

            return {
                data: paginatedResults,
                page: page,
                pageSize: pageSize,
                count: paginatedResults.length,
                totalCount: totalCount,
                totalPages: Math.ceil(totalCount / pageSize)
            };
        } catch (error) {
            console.error('[MASTERLIST] Search error:', error);
            throw error;
        }
    }

    /**
     * Clear masterlist cache
     */
    function clearCache() {
        masterlistCache = null;
        loadPromise = null;
        isLoadingMasterlist = false;
    }

    return {
        searchCards,
        clearCache,
        isLoaded: () => masterlistCache !== null
    };
})();
