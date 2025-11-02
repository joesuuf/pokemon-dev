/**
 * Pokemon TCG Search - Pure JavaScript Application
 * No frameworks, vanilla JS only
 * Secure, accessible, mobile-first
 */

'use strict';

// Application state
const AppState = {
    currentPage: 1,
    totalPages: 1,
    viewMode: 'grid',
    searchQuery: '',
    cards: [],
    isLoading: false
};

// DOM Elements Cache
const DOM = {
    searchForm: null,
    searchInput: null,
    viewModeSelect: null,
    loadingContainer: null,
    loadingText: null,
    timeoutTimer: null,
    foundCards: null,
    errorContainer: null,
    resultsSection: null,
    cardsContainer: null,
    resultCount: null,
    currentPageSpan: null,
    totalPagesSpan: null,
    prevButton: null,
    nextButton: null,
    modal: null,
    modalBody: null
};

// Loading state tracking
let loadingTimer = null;
let timeoutCountdown = null;
let foundCardsList = [];

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);

/**
 * Initialize the application
 */
function initApp() {
    console.log('Initializing Pokemon TCG Search Static Site...');

    // Cache DOM elements
    cacheDOMElements();

    // Set up event listeners
    setupEventListeners();

    // Check for URL parameters (for bookmarking/sharing)
    checkURLParams();

    console.log('App initialized successfully');
}

/**
 * Cache frequently accessed DOM elements
 */
function cacheDOMElements() {
    DOM.searchForm = document.getElementById('search-form');
    DOM.searchInput = document.getElementById('search-input');
    DOM.viewModeSelect = document.getElementById('view-mode');
    DOM.loadingContainer = document.getElementById('loading');
    DOM.loadingText = DOM.loadingContainer?.querySelector('.loading-text');
    DOM.timeoutTimer = document.getElementById('timeout-timer');
    DOM.foundCards = document.getElementById('found-cards');
    DOM.errorContainer = document.getElementById('error');
    DOM.resultsSection = document.getElementById('results');
    DOM.cardsContainer = document.getElementById('cards-container');
    DOM.resultCount = document.getElementById('result-count');
    DOM.currentPageSpan = document.getElementById('current-page');
    DOM.totalPagesSpan = document.getElementById('total-pages');
    DOM.prevButton = document.getElementById('prev-page');
    DOM.nextButton = document.getElementById('next-page');
    DOM.modal = document.getElementById('modal');
    DOM.modalBody = document.getElementById('modal-body');
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    // Search form submission
    DOM.searchForm.addEventListener('submit', handleSearch);

    // View mode change
    DOM.viewModeSelect.addEventListener('change', handleViewModeChange);

    // Pagination
    DOM.prevButton.addEventListener('click', () => changePage(-1));
    DOM.nextButton.addEventListener('click', () => changePage(1));

    // Keyboard navigation for modal
    document.addEventListener('keydown', handleKeyboardNav);

    // Input sanitization
    DOM.searchInput.addEventListener('input', sanitizeInput);
}

/**
 * Sanitize search input to prevent XSS
 */
function sanitizeInput(event) {
    const input = event.target;
    // Remove any HTML tags and dangerous characters
    const sanitized = input.value
        .replace(/<[^>]*>/g, '') // Remove HTML tags
        .replace(/[<>\"']/g, '') // Remove dangerous characters
        .trim();

    if (input.value !== sanitized) {
        input.value = sanitized;
    }
}

/**
 * Handle search form submission
 */
function handleSearch(event) {
    event.preventDefault();

    const query = DOM.searchInput.value.trim();

    if (!query) {
        showError('Please enter a search term');
        return;
    }

    // Validate input (alphanumeric, spaces, hyphens only)
    if (!/^[A-Za-z0-9\s\-]+$/.test(query)) {
        showError('Search term can only contain letters, numbers, spaces, and hyphens');
        return;
    }

    AppState.searchQuery = query;
    AppState.currentPage = 1;

    // Update URL without reloading page
    updateURL();

    // Perform search
    searchCards(query);
}

/**
 * Handle view mode change
 */
function handleViewModeChange(event) {
    AppState.viewMode = event.target.value;
    updateURL();
    renderCards(AppState.cards);
}

/**
 * Search for Pokemon cards
 */
async function searchCards(query) {
    showLoading();
    hideError();
    foundCardsList = [];
    
    // Start timeout countdown (30 seconds)
    const timeoutDuration = 30;
    let timeRemaining = timeoutDuration;
    startTimeoutCountdown(timeoutDuration);

    try {
        const results = await PokemonAPI.searchCards(query, AppState.currentPage);

        // Stop countdown
        stopTimeoutCountdown();

        AppState.cards = results.data;
        AppState.totalPages = results.totalPages;

        // Show found cards as they're discovered (simulate progressive loading)
        if (results.data && results.data.length > 0) {
            displayFoundCards(results.data);
            
            // Apply set theme based on first card found
            if (results.data.length > 0 && typeof SetThemeManager !== 'undefined') {
                SetThemeManager.applySetTheme(document.body, results.data[0]);
            }
        }

        renderCards(results.data);
        updatePagination();
        showResults();

    } catch (error) {
        console.error('Search error:', error);
        stopTimeoutCountdown();
        showError(error.message || 'Failed to search cards. Please try again.');
    } finally {
        hideLoading();
    }
}

/**
 * Start timeout countdown timer
 */
function startTimeoutCountdown(duration) {
    let timeRemaining = duration;
    
    if (DOM.timeoutTimer) {
        updateTimeoutDisplay(timeRemaining);
    }
    
    timeoutCountdown = setInterval(() => {
        timeRemaining--;
        
        if (timeRemaining > 0 && DOM.timeoutTimer) {
            updateTimeoutDisplay(timeRemaining);
        } else {
            stopTimeoutCountdown();
        }
    }, 1000);
}

/**
 * Update timeout display
 */
function updateTimeoutDisplay(seconds) {
    if (!DOM.timeoutTimer) return;
    
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    const timeStr = minutes > 0 
        ? `${minutes}m ${secs}s` 
        : `${secs}s`;
    
    DOM.timeoutTimer.textContent = `?? Time remaining: ${timeStr}`;
    DOM.timeoutTimer.style.display = 'block';
}

/**
 * Stop timeout countdown
 */
function stopTimeoutCountdown() {
    if (timeoutCountdown) {
        clearInterval(timeoutCountdown);
        timeoutCountdown = null;
    }
    if (DOM.timeoutTimer) {
        DOM.timeoutTimer.style.display = 'none';
    }
}

/**
 * Display found cards as they're discovered
 */
function displayFoundCards(cards) {
    if (!DOM.foundCards || !cards || cards.length === 0) return;
    
    // Clear previous
    DOM.foundCards.innerHTML = '';
    
    // Create header
    const header = document.createElement('p');
    header.className = 'found-cards-header';
    header.textContent = `Found ${cards.length} card${cards.length !== 1 ? 's' : ''}:`;
    DOM.foundCards.appendChild(header);
    
    const cardList = document.createElement('div');
    cardList.className = 'found-cards-list';
    DOM.foundCards.appendChild(cardList);
    
    // Show cards progressively (up to 5, then show "and X more")
    const cardsToShow = Math.min(cards.length, 5);
    
    cards.slice(0, cardsToShow).forEach((card, index) => {
        setTimeout(() => {
            const cardItem = document.createElement('div');
            cardItem.className = 'found-card-item';
            
            // Get variation name (set name + card number)
            const setName = card.set?.name || 'Unknown Set';
            const cardNumber = card.number || '?';
            const variationName = `${card.name} (${setName} #${cardNumber})`;
            
            cardItem.textContent = `${index + 1}. ${variationName}`;
            cardList.appendChild(cardItem);
            
            // Rotate gradient based on card's set theme
            if (typeof SetThemeManager !== 'undefined') {
                SetThemeManager.applySetTheme(document.body, card);
            } else if (typeof GradientManager !== 'undefined') {
                // Fallback to general gradient manager
                GradientManager.applyGradient(document.body);
            }
        }, index * 200); // 200ms delay between each card
    });
    
    // Show "and X more" if there are more cards
    if (cards.length > 5) {
        setTimeout(() => {
            const more = document.createElement('div');
            more.className = 'found-cards-more';
            more.textContent = `... and ${cards.length - 5} more`;
            cardList.appendChild(more);
        }, cardsToShow * 200);
    }
}

/**
 * Render cards based on view mode
 */
function renderCards(cards) {
    if (!cards || cards.length === 0) {
        showEmptyState();
        return;
    }

    DOM.cardsContainer.innerHTML = '';
    DOM.resultCount.textContent = cards.length;

    // Update container class based on view mode
    DOM.cardsContainer.className = AppState.viewMode === 'list' ? 'cards-list' : 'cards-grid';

    cards.forEach(card => {
        const cardElement = createCardElement(card);
        DOM.cardsContainer.appendChild(cardElement);
    });
}

/**
 * Create card element based on view mode
 */
function createCardElement(card) {
    if (AppState.viewMode === 'list') {
        return createListCard(card);
    } else if (AppState.viewMode === 'detailed') {
        return createDetailedCard(card);
    } else {
        return createGridCard(card);
    }
}

/**
 * Create grid view card
 */
function createGridCard(card) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card';
    cardDiv.setAttribute('role', 'button');
    cardDiv.setAttribute('tabindex', '0');
    cardDiv.setAttribute('aria-label', `View details for ${UI.escapeHTML(card.name)}`);

    // Safely escape all user content
    const name = UI.escapeHTML(card.name);
    const supertype = UI.escapeHTML(card.supertype || 'Pokemon');
    const hp = UI.escapeHTML(card.hp || 'N/A');
    const rarity = UI.escapeHTML(card.rarity || 'Common');
    const setName = UI.escapeHTML(card.set?.name || 'Unknown Set');

    cardDiv.innerHTML = `
        <div class="card-image-container">
            <img
                src="${UI.escapeHTML(card.images?.small || '')}"
                alt="${name}"
                class="card-image"
                loading="lazy"
                onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\\\'http://www.w3.org/2000/svg\\\\' width=\\\\'245\\\\' height=\\\\'342\\\\'%3E%3Crect fill=\\\\'%23ddd\\\\' width=\\\\'245\\\\' height=\\\\'342\\\\'/%3E%3Ctext x=\\\\'50%25\\\\' y=\\\\'50%25\\\\' text-anchor=\\\\'middle\\\\' dy=\\\\'.3em\\\\' fill=\\\\'%23999\\\\'%3ENo Image%3C/text%3E%3C/svg%3E'"
            >
        </div>
        <div class="card-content">
            <div class="card-header">
                <h3 class="card-name">${name}</h3>
                <p class="card-supertype">${supertype}</p>
            </div>
            ${card.types ? `
                <div class="card-types">
                    ${card.types.map(type => `<span class="type-badge type-${UI.escapeHTML(type.toLowerCase())}">${UI.escapeHTML(type)}</span>`).join('')}
                </div>
            ` : ''}
            <div class="card-stats">
                <div class="card-stat">
                    <span class="card-stat-label">HP:</span>
                    <span class="card-stat-value">${hp}</span>
                </div>
            </div>
            <div class="card-footer">
                <p class="card-set">${setName}</p>
                <span class="card-rarity rarity-${UI.escapeHTML(rarity.toLowerCase().replace(/\s+/g, '-'))}">${rarity}</span>
            </div>
        </div>
    `;

    cardDiv.addEventListener('click', () => showCardDetails(card));
    cardDiv.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            showCardDetails(card);
        }
    });

    return cardDiv;
}

/**
 * Create list view card
 */
function createListCard(card) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card-list-item';

    const name = UI.escapeHTML(card.name);
    const supertype = UI.escapeHTML(card.supertype || 'Pokemon');
    const hp = UI.escapeHTML(card.hp || 'N/A');
    const setName = UI.escapeHTML(card.set?.name || 'Unknown Set');

    cardDiv.innerHTML = `
        <img
            src="${UI.escapeHTML(card.images?.small || '')}"
            alt="${name}"
            class="card-list-image"
            loading="lazy"
        >
        <div class="card-list-content">
            <h3>${name}</h3>
            <p>${supertype} | HP: ${hp}</p>
            <p class="text-muted">${setName}</p>
        </div>
    `;

    cardDiv.addEventListener('click', () => showCardDetails(card));

    return cardDiv;
}

/**
 * Create detailed view card
 */
function createDetailedCard(card) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'card-detailed';

    // Render full card details
    cardDiv.innerHTML = UI.renderCardDetails(card);

    return cardDiv;
}

/**
 * Show card details in modal
 */
function showCardDetails(card) {
    DOM.modalBody.innerHTML = UI.renderCardDetails(card);
    DOM.modal.classList.remove('hidden');
    DOM.modal.setAttribute('aria-hidden', 'false');

    // Trap focus in modal
    const focusableElements = DOM.modal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    if (focusableElements.length > 0) {
        focusableElements[0].focus();
    }
}

/**
 * Close modal
 */
function closeModal() {
    DOM.modal.classList.add('hidden');
    DOM.modal.setAttribute('aria-hidden', 'true');
}

// Make closeModal globally accessible
window.closeModal = closeModal;

/**
 * Handle keyboard navigation
 */
function handleKeyboardNav(event) {
    // Close modal on Escape
    if (event.key === 'Escape' && !DOM.modal.classList.contains('hidden')) {
        closeModal();
    }
}

/**
 * Change page
 */
function changePage(direction) {
    const newPage = AppState.currentPage + direction;

    if (newPage < 1 || newPage > AppState.totalPages) {
        return;
    }

    AppState.currentPage = newPage;
    updateURL();
    searchCards(AppState.searchQuery);

    // Scroll to top of results
    DOM.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update pagination controls
 */
function updatePagination() {
    DOM.currentPageSpan.textContent = AppState.currentPage;
    DOM.totalPagesSpan.textContent = AppState.totalPages;

    DOM.prevButton.disabled = AppState.currentPage <= 1;
    DOM.nextButton.disabled = AppState.currentPage >= AppState.totalPages;
}

/**
 * Update URL with current state (for bookmarking/sharing)
 */
function updateURL() {
    const params = new URLSearchParams();

    if (AppState.searchQuery) {
        params.set('q', AppState.searchQuery);
    }
    if (AppState.currentPage > 1) {
        params.set('page', AppState.currentPage);
    }
    if (AppState.viewMode !== 'grid') {
        params.set('view', AppState.viewMode);
    }

    const newURL = params.toString() ? `?${params.toString()}` : window.location.pathname;
    window.history.replaceState({}, '', newURL);
}

/**
 * Check URL parameters on page load
 */
function checkURLParams() {
    const params = new URLSearchParams(window.location.search);

    const query = params.get('q');
    const page = parseInt(params.get('page')) || 1;
    const view = params.get('view') || 'grid';

    if (query) {
        DOM.searchInput.value = query;
        AppState.searchQuery = query;
        AppState.currentPage = page;
        AppState.viewMode = view;
        DOM.viewModeSelect.value = view;

        searchCards(query);
    }
}

/**
 * Show/Hide UI states
 */
function showLoading() {
    AppState.isLoading = true;
    DOM.loadingContainer.classList.remove('hidden');
    DOM.loadingContainer.setAttribute('aria-busy', 'true');
    
    // Clear found cards
    if (DOM.foundCards) {
        DOM.foundCards.innerHTML = '';
    }
    
    // Update loading text
    if (DOM.loadingText) {
        DOM.loadingText.textContent = 'Searching for cards...';
    }
}

function hideLoading() {
    AppState.isLoading = false;
    stopTimeoutCountdown();
    DOM.loadingContainer.classList.add('hidden');
    DOM.loadingContainer.setAttribute('aria-busy', 'false');
    
    // Clear found cards after a brief delay
    setTimeout(() => {
        if (DOM.foundCards) {
            DOM.foundCards.innerHTML = '';
        }
    }, 500);
}

function showError(message) {
    DOM.errorContainer.classList.remove('hidden');
    DOM.errorContainer.querySelector('.error-message').textContent = message;
}

function hideError() {
    DOM.errorContainer.classList.add('hidden');
}

// Make hideError globally accessible
window.hideError = hideError;

function showResults() {
    DOM.resultsSection.classList.remove('hidden');
}

function showEmptyState() {
    DOM.cardsContainer.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">??</div>
            <p class="empty-state-text">No cards found. Try a different search term.</p>
        </div>
    `;
    DOM.resultCount.textContent = '0';
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHTML(str) {
    if (!str) return '';
    return UI.escapeHTML(str);
}
