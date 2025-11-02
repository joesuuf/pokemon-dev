/**
 * Set Theme Manager - Manages gradient themes for different Pokemon TCG sets
 * Preloads and caches set-specific gradient schemes
 */

const SetThemeManager = (function() {
    const themes = new Map();
    let currentTheme = null;
    
    // Pokemon TCG Set abbreviations and their gradient themes
    // Each set gets a unique color scheme based on the set's theme
    const SET_THEMES = {
        // Base sets
        'BS': { colors: ['#CC0000', '#FFDE00', '#003DA5'], angle: 135 }, // Base Set - Classic red/yellow/blue
        'BS1': { colors: ['#CC0000', '#FFDE00', '#003DA5'], angle: 135 }, // Base Set 1
        'BS2': { colors: ['#990000', '#FFDE00', '#002966'], angle: 135 }, // Base Set 2 - Darker
        
        // Sword & Shield era
        'SWSH': { colors: ['#1a237e', '#e53935', '#ffd54f'], angle: 135 }, // Sword & Shield
        'SWSH1': { colors: ['#283593', '#e53935', '#ffd54f'], angle: 135 }, // Sword & Shield Base
        'SWSH2': { colors: ['#1565c0', '#d32f2f', '#ffc107'], angle: 140 }, // Rebel Clash
        'SWSH3': { colors: ['#0d47a1', '#c62828', '#ffb300'], angle: 130 }, // Darkness Ablaze
        'SWSH4': { colors: ['#0277bd', '#b71c1c', '#ffa000'], angle: 138 }, // Vivid Voltage
        'SWSH5': { colors: ['#01579b', '#ad1457', '#ff8f00'], angle: 142 }, // Shining Fates
        'SWSH6': { colors: ['#004d40', '#880e4f', '#ff6f00'], angle: 128 }, // Battle Styles
        'SWSH7': { colors: ['#006064', '#4a148c', '#e65100'], angle: 136 }, // Chilling Reign
        'SWSH8': { colors: ['#00796b', '#6a1b9a', '#ff5722'], angle: 134 }, // Evolving Skies
        'SWSH9': { colors: ['#00897b', '#7b1fa2', '#ff9800'], angle: 132 }, // Fusion Strike
        'SWSH10': { colors: ['#00695c', '#8e24aa', '#f57c00'], angle: 144 }, // Brilliant Stars
        'SWSH11': { colors: ['#005249', '#9c27b0', '#ef6c00'], angle: 130 }, // Astral Radiance
        'SWSH12': { colors: ['#004d40', '#ab47bc', '#e65100'], angle: 138 }, // Lost Origin
        
        // Scarlet & Violet era
        'SVE': { colors: ['#d32f2f', '#1976d2', '#388e3c'], angle: 135 }, // Scarlet & Violet - Base
        'SVI': { colors: ['#c62828', '#1565c0', '#2e7d32'], angle: 135 }, // Scarlet & Violet - Base (alt)
        'SVI1': { colors: ['#d32f2f', '#1976d2', '#388e3c'], angle: 135 }, // Base Set
        'SVI2': { colors: ['#ad1457', '#0d47a1', '#1b5e20'], angle: 140 }, // Paldea Evolved
        'SVI3': { colors: ['#880e4f', '#0277bd', '#33691e'], angle: 130 }, // Obsidian Flames
        'SVI4': { colors: ['#6a1b9a', '#01579b', '#558b2f'], angle: 138 }, // 151
        'SVI5': { colors: ['#4a148c', '#004d40', '#689f38'], angle: 142 }, // Paradox Rift
        'SVI6': { colors: ['#7b1fa2', '#006064', '#827717'], angle: 128 }, // Paldean Fates
        'SVI7': { colors: ['#8e24aa', '#00796b', '#33691e'], angle: 136 }, // Temporal Forces
        
        // Sun & Moon era
        'SUM': { colors: ['#ff6f00', '#0277bd', '#1b5e20'], angle: 135 }, // Sun & Moon
        'SUM1': { colors: ['#ff6f00', '#0277bd', '#1b5e20'], angle: 135 }, // Base Set
        'SUM2': { colors: ['#e65100', '#01579b', '#33691e'], angle: 140 }, // Guardians Rising
        'SUM3': { colors: ['#f57c00', '#004d40', '#558b2f'], angle: 130 }, // Burning Shadows
        
        // XY era
        'XY': { colors: ['#e53935', '#1a237e', '#ffd54f'], angle: 135 }, // XY
        'XY1': { colors: ['#e53935', '#1a237e', '#ffd54f'], angle: 135 }, // Base Set
        
        // Black & White era
        'BW': { colors: ['#424242', '#e0e0e0', '#212121'], angle: 135 }, // Black & White
        'BW1': { colors: ['#424242', '#e0e0e0', '#212121'], angle: 135 }, // Base Set
        
        // Default fallback
        'default': { colors: ['#CC0000', '#FFDE00', '#003DA5'], angle: 135 }
    };
    
    /**
     * Generate CSS gradient from theme
     */
    function generateGradient(theme, variation = 0) {
        const [color1, color2, color3] = theme.colors;
        const angle = theme.angle + (variation * 2); // Slight variation
        
        // Create 10 variations for smooth animation
        const variations = [
            { angle: angle, stops: [color1, color2, color3], pos: [0, 50, 100] },
            { angle: angle, stops: [color1, color2, color3], pos: [0, 40, 100] },
            { angle: angle + 2, stops: [color1, color2, color3], pos: [0, 45, 100] },
            { angle: angle, stops: [color1, color2, color3], pos: [0, 50, 90] },
            { angle: angle - 2, stops: [color1, color2, color3], pos: [0, 50, 100] },
            { angle: angle, stops: [color1, color2, color3], pos: [0, 48, 100] },
            { angle: angle + 3, stops: [color1, color2, color3], pos: [0, 52, 100] },
            { angle: angle, stops: [color1, color2, color3], pos: [0, 45, 100] },
            { angle: angle - 3, stops: [color1, color2, color3], pos: [0, 50, 100] },
            { angle: angle, stops: [color1, color2, color3], pos: [0, 50, 95] }
        ];
        
        return variations.map(v => {
            const stops = v.stops.map((color, i) => 
                `${color} ${v.pos[i]}%`
            ).join(', ');
            return `linear-gradient(${v.angle}deg, ${stops})`;
        });
    }
    
    /**
     * Get set abbreviation from card data
     */
    function getSetAbbreviation(card) {
        if (!card || !card.set) return 'default';
        
        // Try to get abbreviation from set object
        if (card.set.id) {
            // Extract abbreviation from set ID (format: "sv1", "swsh1", etc.)
            const setId = card.set.id.toLowerCase();
            const match = setId.match(/^(swsh|svi|sve|sum|xy|bw)(\d+)?/);
            if (match) {
                const base = match[1].toUpperCase();
                const num = match[2] || '';
                return base + num;
            }
        }
        
        // Fallback: try to extract from set name
        if (card.set.name) {
            const setName = card.set.name.toLowerCase();
            // Common patterns
            if (setName.includes('scarlet') || setName.includes('violet')) {
                return 'SVI';
            }
            if (setName.includes('sword') || setName.includes('shield')) {
                return 'SWSH';
            }
            if (setName.includes('sun') || setName.includes('moon')) {
                return 'SUM';
            }
        }
        
        return 'default';
    }
    
    /**
     * Preload all set themes
     */
    function preloadThemes() {
        Object.keys(SET_THEMES).forEach(abbrev => {
            const theme = SET_THEMES[abbrev];
            const gradients = generateGradient(theme);
            themes.set(abbrev, {
                abbreviation: abbrev,
                theme: theme,
                gradients: gradients,
                currentIndex: 0
            });
        });
        
        console.log(`Preloaded ${themes.size} set themes with gradients`);
        return themes;
    }
    
    /**
     * Get gradient for a specific set
     */
    function getSetGradient(setAbbrev) {
        const themeData = themes.get(setAbbrev) || themes.get('default');
        if (!themeData) return null;
        
        const gradient = themeData.gradients[themeData.currentIndex];
        themeData.currentIndex = (themeData.currentIndex + 1) % themeData.gradients.length;
        
        return {
            gradient: gradient,
            abbreviation: themeData.abbreviation
        };
    }
    
    /**
     * Apply set theme to element based on card
     */
    function applySetTheme(element, card) {
        const setAbbrev = getSetAbbreviation(card);
        const gradientData = getSetGradient(setAbbrev);
        
        if (gradientData && element) {
            element.style.background = gradientData.gradient;
            element.style.backgroundAttachment = 'fixed';
            currentTheme = setAbbrev;
            return setAbbrev;
        }
        
        return null;
    }
    
    /**
     * Get current theme abbreviation
     */
    function getCurrentTheme() {
        return currentTheme || 'default';
    }
    
    /**
     * Initialize theme manager
     */
    function init() {
        preloadThemes();
    }
    
    return {
        init,
        applySetTheme,
        getSetGradient,
        getSetAbbreviation,
        getCurrentTheme,
        SET_THEMES,
        themes
    };
})();

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', SetThemeManager.init);
} else {
    SetThemeManager.init();
}
