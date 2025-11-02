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

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);

/**
 * Initialize the application
 */
function initApp() {
    console.log('Initializing Pokemon TCG Search v2...');

    // Cache DOM elements
    cacheDOMElements();

    // Set up event listeners
    setupEventListeners();

    // Apply random gradient background
    applyRandomGradient();

    // Check for URL parameters (for bookmarking/sharing)
    checkURLParams();

    console.log('App initialized successfully');
}

/**
 * Apply random gradient background
 */
function applyRandomGradient() {
    // Define gradient variations using Pokemon brand colors
    const gradients = [
        'linear-gradient(135deg, #CC0000 0%, #FFDE00 50%, #003DA5 100%)',
        'linear-gradient(135deg, #CC0000 0%, #FFDE00 40%, #003DA5 100%)',
        'linear-gradient(135deg, #FF0000 0%, #FFDE00 35%, #003DA5 100%)',
        'linear-gradient(135deg, #CC0000 0%, #FFDE00 45%, #0066CC 90%)',
        'linear-gradient(140deg, #CC0000 0%, #FFDE00 50%, #003DA5 100%)',
        'linear-gradient(135deg, #FF0000 0%, #FFFF00 50%, #0066CC 100%)',
        'linear-gradient(130deg, #CC0000 0%, #FFDE00 50%, #003DA5 100%)',
        'linear-gradient(135deg, #990000 0%, #FFDE00 45%, #002966 100%)',
        'linear-gradient(138deg, #CC0000 0%, #FFDE00 48%, #003DA5 100%)',
        'linear-gradient(135deg, #CC0000 0%, #FFDE00 52%, #003DA5 100%)'
    ];
    
    const randomGradient = gradients[Math.floor(Math.random() * gradients.length)];
    document.body.style.background = randomGradient;
    document.body.style.backgroundAttachment = 'fixed';
}

/**
 * Cache frequently accessed DOM elements
 */
function cacheDOMElements() {
    DOM.searchForm = document.getElementById('search-form');
    DOM.searchInput = document.getElementById('search-input');
    DOM.viewModeSelect = document.getElementById('view-mode');
    DOM.loadingContainer = document.getElementById('loading');
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

    try {
        const results = await PokemonAPI.searchCards(query, AppState.currentPage);

        AppState.cards = results.data;
        AppState.totalPages = results.totalPages;

        renderCards(results.data);
        updatePagination();
        showResults();

    } catch (error) {
        console.error('Search error:', error);
        showError(error.message || 'Failed to search cards. Please try again.');
    } finally {
        hideLoading();
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
    cardDiv.setAttribute('aria-label', `View details for ${escapeHTML(card.name)}`);

    // Safely escape all user content
    const name = escapeHTML(card.name);
    const supertype = escapeHTML(card.supertype || 'Pokemon');
    const hp = escapeHTML(card.hp || 'N/A');
    const rarity = escapeHTML(card.rarity || 'Common');
    const setName = escapeHTML(card.set?.name || 'Unknown Set');

    cardDiv.innerHTML = `
        <div class="card-image-container">
            <img
                src="${escapeHTML(card.images?.small || '')}"
                alt="${name}"
                class="card-image"
                loading="lazy"
                onerror="this.src='data:image/svg+xml,%3Csvg xmlns=\\'http://www.w3.org/2000/svg\\' width=\\'245\\' height=\\'342\\'%3E%3Crect fill=\\'%23ddd\\' width=\\'245\\' height=\\'342\\'/%3E%3Ctext x=\\'50%25\\' y=\\'50%25\\' text-anchor=\\'middle\\' dy=\\'.3em\\' fill=\\'%23999\\'%3ENo Image%3C/text%3E%3C/svg%3E'"
            >
        </div>
        <div class="card-content">
            <div class="card-header">
                <h3 class="card-name">${name}</h3>
                <p class="card-supertype">${supertype}</p>
            </div>
            ${card.types ? `
                <div class="card-types">
                    ${card.types.map(type => `<span class="type-badge type-${escapeHTML(type.toLowerCase())}">${escapeHTML(type)}</span>`).join('')}
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
                <span class="card-rarity rarity-${escapeHTML(rarity.toLowerCase().replace(/\s+/g, '-'))}">${rarity}</span>
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

    const name = escapeHTML(card.name);
    const supertype = escapeHTML(card.supertype || 'Pokemon');
    const hp = escapeHTML(card.hp || 'N/A');
    const setName = escapeHTML(card.set?.name || 'Unknown Set');

    cardDiv.innerHTML = `
        <img
            src="${escapeHTML(card.images?.small || '')}"
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
}

function hideLoading() {
    AppState.isLoading = false;
    DOM.loadingContainer.classList.add('hidden');
    DOM.loadingContainer.setAttribute('aria-busy', 'false');
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

    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
