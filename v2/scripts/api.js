/**
 * Pokemon TCG API Client
 * Secure, vanilla JavaScript implementation
 */

'use strict';

const PokemonAPI = (function() {
    // API Configuration
    const CONFIG = {
        baseURL: 'https://api.pokemontcg.io/v2',
        pageSize: 20,
        timeout: 10000 // 10 seconds
    };

    /**
     * Make a secure API request
     */
    async function makeRequest(endpoint, params = {}) {
        // Build query string securely
        const queryParams = new URLSearchParams();

        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                queryParams.append(key, params[key]);
            }
        });

        const url = `${CONFIG.baseURL}/${endpoint}?${queryParams.toString()}`;

        // Create AbortController for timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.timeout);

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    // Note: In production, API key should come from backend proxy
                    // Never expose API keys in frontend code
                },
                signal: controller.signal,
                mode: 'cors',
                credentials: 'omit' // Don't send cookies for security
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(getErrorMessage(response.status));
            }

            const data = await response.json();
            return data;

        } catch (error) {
            clearTimeout(timeoutId);

            if (error.name === 'AbortError') {
                throw new Error('Request timeout. Please check your connection and try again.');
            }

            throw error;
        }
    }

    /**
     * Get user-friendly error message based on status code
     */
    function getErrorMessage(status) {
        const messages = {
            400: 'Invalid search query. Please check your input.',
            401: 'Authentication failed. Please contact support.',
            403: 'Access denied. You may have exceeded rate limits.',
            404: 'No results found.',
            429: 'Too many requests. Please wait a moment and try again.',
            500: 'Server error. Please try again later.',
            503: 'Service unavailable. Please try again later.'
        };

        return messages[status] || `Request failed with status ${status}`;
    }

    /**
     * Search for cards
     */
    async function searchCards(query, page = 1) {
        // Sanitize and validate query
        const sanitizedQuery = sanitizeQuery(query);

        if (!sanitizedQuery) {
            throw new Error('Invalid search query');
        }

        const params = {
            q: `name:${sanitizedQuery}*`,
            page: page,
            pageSize: CONFIG.pageSize,
            orderBy: 'name'
        };

        try {
            const response = await makeRequest('cards', params);

            return {
                data: response.data || [],
                page: response.page || 1,
                pageSize: response.pageSize || CONFIG.pageSize,
                count: response.count || 0,
                totalCount: response.totalCount || 0,
                totalPages: Math.ceil((response.totalCount || 0) / CONFIG.pageSize)
            };

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get card by ID
     */
    async function getCardById(id) {
        // Validate ID format (Pokemon TCG IDs are alphanumeric with hyphens)
        if (!/^[a-zA-Z0-9\-]+$/.test(id)) {
            throw new Error('Invalid card ID format');
        }

        try {
            const response = await makeRequest(`cards/${id}`);
            return response.data;

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Get random cards
     */
    async function getRandomCards(count = 10) {
        const params = {
            page: 1,
            pageSize: Math.min(count, 250), // API limit
            orderBy: 'random'
        };

        try {
            const response = await makeRequest('cards', params);
            return response.data || [];

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Search by type
     */
    async function searchByType(type, page = 1) {
        const validTypes = [
            'Grass', 'Fire', 'Water', 'Lightning', 'Psychic',
            'Fighting', 'Darkness', 'Metal', 'Dragon', 'Fairy', 'Colorless'
        ];

        if (!validTypes.includes(type)) {
            throw new Error('Invalid Pokemon type');
        }

        const params = {
            q: `types:${type}`,
            page: page,
            pageSize: CONFIG.pageSize,
            orderBy: 'name'
        };

        try {
            const response = await makeRequest('cards', params);

            return {
                data: response.data || [],
                totalPages: Math.ceil((response.totalCount || 0) / CONFIG.pageSize)
            };

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    /**
     * Sanitize search query to prevent injection attacks
     */
    function sanitizeQuery(query) {
        if (!query || typeof query !== 'string') {
            return '';
        }

        // Remove any special characters that could be used for injection
        // Allow only alphanumeric, spaces, and hyphens
        return query
            .replace(/[^a-zA-Z0-9\s\-]/g, '')
            .trim()
            .substring(0, 100); // Limit length
    }

    /**
     * Validate URL to prevent open redirect vulnerabilities
     */
    function isValidURL(url) {
        try {
            const parsed = new URL(url);
            // Only allow https URLs from trusted domains
            return parsed.protocol === 'https:' &&
                   (parsed.hostname.endsWith('pokemontcg.io') ||
                    parsed.hostname.endsWith('pokemon.com'));
        } catch {
            return false;
        }
    }

    // Public API
    return {
        searchCards,
        getCardById,
        getRandomCards,
        searchByType,
        sanitizeQuery,
        isValidURL
    };
})();

// Prevent modification of API object
Object.freeze(PokemonAPI);
