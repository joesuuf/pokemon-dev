/**
 * Set Theme Manager - Manages gradient themes for different Pokemon TCG sets
 * Uses comprehensive lookup table from set-theme-lookup.js
 */

// Import lookup table (loaded before this script)
const SET_THEMES = typeof POKEMON_TCG_SET_THEMES !== 'undefined' 
    ? POKEMON_TCG_SET_THEMES 
    : {};

const SetThemeManager = (function() {
    const themes = new Map();
    let currentTheme = null;
    
    /**
     * Generate CSS gradient from theme (10 variations)
     */
    function generateGradient(theme, variation = 0) {
        const [color1, color2, color3] = theme.colors;
        const baseAngle = theme.angle || 135;
        
        // Create 10 variations for smooth animation
        const variations = [
            { angle: baseAngle, pos: [0, 50, 100] },
            { angle: baseAngle, pos: [0, 40, 100] },
            { angle: baseAngle + 2, pos: [0, 45, 100] },
            { angle: baseAngle, pos: [0, 50, 90] },
            { angle: baseAngle - 2, pos: [0, 50, 100] },
            { angle: baseAngle, pos: [0, 48, 100] },
            { angle: baseAngle + 3, pos: [0, 52, 100] },
            { angle: baseAngle, pos: [0, 45, 100] },
            { angle: baseAngle - 3, pos: [0, 50, 100] },
            { angle: baseAngle, pos: [0, 50, 95] }
        ];
        
        return variations.map(v => {
            const stops = `${color1} ${v.pos[0]}%, ${color2} ${v.pos[1]}%, ${color3} ${v.pos[2]}%`;
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
            
            // Handle various formats
            const patterns = [
                /^(sv1|sv2|sv3|sv4|sv5|sv6|sv7|sv8|sv9|svi|sve)$/,
                /^(swsh|swsh1|swsh2|swsh3|swsh4|swsh5|swsh6|swsh7|swsh8|swsh9|swsh10|swsh11|swsh12|swsh13|swsh14)$/,
                /^(sum|sum1|sum2|sum3|sum4|sum5|sum6|sum7|sum8|sum9|sum10|sum11|sum12)$/,
                /^(xy|xy1|xy2|xy3|xy4|xy5|xy6|xy7|xy8|xy9|xy10|xy11|xy12)$/,
                /^(bw|bw1|bw2|bw3|bw4|bw5|bw6|bw7|bw8|bw9|bw10|bw11)$/,
                /^(hgss|hgss1|hgss2|hgss3|hgss4)$/,
                /^(pl|pl1|pl2|pl3|pl4)$/,
                /^(dp|dp1|dp2|dp3|dp4|dp5|dp6|dp7)$/,
                /^(ex|ex1|ex2|ex3|ex4|ex5|ex6|ex7|ex8|ex9|ex10|ex11|ex12|ex13|ex14|ex15|ex16)$/,
                /^(n|n1|n2|n3|n4)$/,
                /^(bs|bs1|bs2)$/,
                /^(jng|fos|tr|g1|g2)$/
            ];
            
            for (const pattern of patterns) {
                const match = setId.match(pattern);
                if (match) {
                    return match[0].toUpperCase();
                }
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
     * Preload all set themes from lookup table
     */
    function preloadThemes() {
        Object.keys(SET_THEMES).forEach(abbrev => {
            const theme = SET_THEMES[abbrev];
            const gradients = generateGradient(theme);
            themes.set(abbrev, {
                abbreviation: abbrev,
                name: theme.name,
                era: theme.era,
                route: theme.route,
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
            abbreviation: themeData.abbreviation,
            name: themeData.name,
            era: themeData.era,
            route: themeData.route
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
     * Get theme info for a set abbreviation
     */
    function getThemeInfo(abbrev) {
        return themes.get(abbrev) || themes.get('default');
    }
    
    /**
     * Get all available themes
     */
    function getAllThemes() {
        return Array.from(themes.values()).map(t => ({
            abbreviation: t.abbreviation,
            name: t.name,
            era: t.era,
            route: t.route
        }));
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
        getThemeInfo,
        getAllThemes,
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
