/**
 * UI Helper Functions
 * Secure rendering and DOM manipulation
 */

'use strict';

const UI = (function() {
    /**
     * Escape HTML to prevent XSS attacks
     */
    function escapeHTML(str) {
        if (!str) return '';

        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /**
     * Sanitize URL to prevent javascript: and data: URIs
     */
    function sanitizeURL(url) {
        if (!url || typeof url !== 'string') {
            return '';
        }

        // Only allow http and https protocols
        const lowerURL = url.toLowerCase().trim();
        if (!lowerURL.startsWith('http://') && !lowerURL.startsWith('https://')) {
            return '';
        }

        return url;
    }

    /**
     * Create safe image element
     */
    function createImage(src, alt, className = '') {
        const img = document.createElement('img');
        img.src = sanitizeURL(src) || 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'245\' height=\'342\'%3E%3Crect fill=\'%23ddd\' width=\'245\' height=\'342\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\'%3ENo Image%3C/text%3E%3C/svg%3E';
        img.alt = escapeHTML(alt);
        if (className) {
            img.className = className;
        }
        img.loading = 'lazy';

        // Add error handler
        img.onerror = function() {
            this.src = 'data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'245\' height=\'342\'%3E%3Crect fill=\'%23ddd\' width=\'245\' height=\'342\'/%3E%3Ctext x=\'50%25\' y=\'50%25\' text-anchor=\'middle\' dy=\'.3em\' fill=\'%23999\'%3EImage Error%3C/text%3E%3C/svg%3E';
        };

        return img;
    }

    /**
     * Render full card details
     */
    function renderCardDetails(card) {
        const name = escapeHTML(card.name);
        const supertype = escapeHTML(card.supertype || 'Pokemon');
        const hp = escapeHTML(card.hp || 'N/A');
        const rarity = escapeHTML(card.rarity || 'Common');
        const setName = escapeHTML(card.set?.name || 'Unknown Set');
        const artist = escapeHTML(card.artist || 'Unknown');
        const number = escapeHTML(card.number || '?');
        const total = escapeHTML(card.set?.printedTotal || '?');

        let detailsHTML = `
            <div class="card-detailed">
                <div class="card-detailed-header">
                    <div class="card-detailed-image">
                        <img
                            src="${escapeHTML(card.images?.large || card.images?.small || '')}"
                            alt="${name}"
                            style="max-width: 100%; height: auto; border-radius: 8px;"
                        >
                    </div>
                    <div class="card-detailed-info">
                        <h2>${name}</h2>
                        <p><strong>Type:</strong> ${supertype}</p>
                        ${card.hp ? `<p><strong>HP:</strong> ${hp}</p>` : ''}
                        ${card.types ? `
                            <div class="card-types" style="margin: 1rem 0;">
                                ${card.types.map(type =>
                                    `<span class="type-badge type-${escapeHTML(type.toLowerCase())}">${escapeHTML(type)}</span>`
                                ).join('')}
                            </div>
                        ` : ''}

                        <p><strong>Set:</strong> ${setName}</p>
                        <p><strong>Card Number:</strong> ${number}/${total}</p>
                        <p><strong>Rarity:</strong> <span class="card-rarity rarity-${escapeHTML(rarity.toLowerCase().replace(/\s+/g, '-'))}">${rarity}</span></p>
                        <p><strong>Artist:</strong> ${artist}</p>
                    </div>
                </div>
        `;

        // Abilities
        if (card.abilities && card.abilities.length > 0) {
            detailsHTML += '<div class="card-abilities"><h3>Abilities</h3>';
            card.abilities.forEach(ability => {
                const abilityName = escapeHTML(ability.name);
                const abilityText = escapeHTML(ability.text || '');
                const abilityType = escapeHTML(ability.type || '');

                detailsHTML += `
                    <div class="ability-item">
                        <div class="ability-name">${abilityName} ${abilityType ? `(${abilityType})` : ''}</div>
                        <div class="ability-text">${abilityText}</div>
                    </div>
                `;
            });
            detailsHTML += '</div>';
        }

        // Attacks
        if (card.attacks && card.attacks.length > 0) {
            detailsHTML += '<div class="card-attacks"><h3>Attacks</h3>';
            card.attacks.forEach(attack => {
                const attackName = escapeHTML(attack.name);
                const attackText = escapeHTML(attack.text || '');
                const damage = escapeHTML(attack.damage || '');

                detailsHTML += `
                    <div class="attack-item">
                        <div class="attack-name">
                            ${attackName}
                            ${damage ? `<span style="float: right;">${damage}</span>` : ''}
                        </div>
                        ${attack.cost ? `
                            <div style="margin: 0.5rem 0;">
                                ${attack.cost.map(type =>
                                    `<span class="type-badge type-${escapeHTML(type.toLowerCase())}" style="font-size: 0.75rem;">${escapeHTML(type)}</span>`
                                ).join(' ')}
                            </div>
                        ` : ''}
                        <div class="attack-text">${attackText}</div>
                    </div>
                `;
            });
            detailsHTML += '</div>';
        }

        // Weaknesses
        if (card.weaknesses && card.weaknesses.length > 0) {
            detailsHTML += '<div style="margin-top: 1rem;"><h4>Weaknesses</h4><div class="card-types">';
            card.weaknesses.forEach(weakness => {
                const type = escapeHTML(weakness.type);
                const value = escapeHTML(weakness.value);
                detailsHTML += `<span class="type-badge type-${escapeHTML(type.toLowerCase())}">${type} ${value}</span>`;
            });
            detailsHTML += '</div></div>';
        }

        // Resistances
        if (card.resistances && card.resistances.length > 0) {
            detailsHTML += '<div style="margin-top: 1rem;"><h4>Resistances</h4><div class="card-types">';
            card.resistances.forEach(resistance => {
                const type = escapeHTML(resistance.type);
                const value = escapeHTML(resistance.value);
                detailsHTML += `<span class="type-badge type-${escapeHTML(type.toLowerCase())}">${type} ${value}</span>`;
            });
            detailsHTML += '</div></div>';
        }

        // Retreat Cost
        if (card.retreatCost && card.retreatCost.length > 0) {
            detailsHTML += `
                <div style="margin-top: 1rem;">
                    <h4>Retreat Cost</h4>
                    <div class="card-types">
                        ${card.retreatCost.map(type =>
                            `<span class="type-badge type-${escapeHTML(type.toLowerCase())}">${escapeHTML(type)}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
        }

        // Rules
        if (card.rules && card.rules.length > 0) {
            detailsHTML += '<div style="margin-top: 1rem; padding: 1rem; background: #f5f5f5; border-radius: 8px;"><h4>Special Rules</h4><ul>';
            card.rules.forEach(rule => {
                detailsHTML += `<li>${escapeHTML(rule)}</li>`;
            });
            detailsHTML += '</ul></div>';
        }

        detailsHTML += '</div>';

        return detailsHTML;
    }

    /**
     * Show toast notification
     */
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.setAttribute('role', 'status');
        toast.setAttribute('aria-live', 'polite');

        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    /**
     * Format date safely
     */
    function formatDate(dateString) {
        if (!dateString) return 'Unknown';

        try {
            const date = new Date(dateString);
            if (isNaN(date.getTime())) {
                return 'Invalid Date';
            }
            return date.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch {
            return 'Invalid Date';
        }
    }

    /**
     * Debounce function for performance
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Throttle function for performance
     */
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // Public API
    return {
        escapeHTML,
        sanitizeURL,
        createImage,
        renderCardDetails,
        showToast,
        formatDate,
        debounce,
        throttle
    };
})();

// Prevent modification
Object.freeze(UI);

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
