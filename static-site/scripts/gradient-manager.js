/**
 * Gradient Manager - Handles preloading, caching, and rotation
 */

const GradientManager = (function() {
    const GRADIENT_COUNT = 10;
    const gradients = [];
    let currentGradientIndex = 0;
    let loadedGradients = 0;
    
    // Pokemon brand colors
    const COLORS = {
        red: '#CC0000',
        yellow: '#FFDE00',
        blue: '#003DA5',
        redLight: '#FF0000',
        redDark: '#990000',
        blueLight: '#0066CC',
        blueDark: '#002966',
        yellowLight: '#FFFF00',
        yellowDark: '#CCAA00'
    };
    
    /**
     * Preload all gradients (CSS gradients are instant, but we cache the strings)
     */
    function preloadGradients() {
        for (let i = 0; i < GRADIENT_COUNT; i++) {
            gradients.push({
                index: i,
                cssGradient: getCSSGradient(i)
            });
        }
        console.log('All gradients cached and ready');
        return gradients;
    }
    
    /**
     * Get next gradient (rotates through all gradients)
     */
    function getNextGradient() {
        const index = currentGradientIndex;
        currentGradientIndex = (currentGradientIndex + 1) % GRADIENT_COUNT;
        return {
            index: index,
            cssGradient: getCSSGradient(index)
        };
    }
    
    /**
     * Apply gradient to element using CSS
     */
    function applyGradient(element) {
        const gradient = getNextGradient();
        if (gradient && element) {
            const cssGradient = getCSSGradient(gradient.index);
            element.style.background = cssGradient;
            element.style.backgroundAttachment = 'fixed';
        }
    }
    
    /**
     * Get CSS gradient string for direct CSS use
     */
    function getCSSGradient(index) {
        const variation = [
            { angle: 135, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 50 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 40 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.redLight, pos: 0 },
                { color: COLORS.yellow, pos: 35 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 45 },
                { color: COLORS.blueLight, pos: 90 }
            ]},
            { angle: 140, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 50 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.redLight, pos: 0 },
                { color: COLORS.yellowLight, pos: 50 },
                { color: COLORS.blueLight, pos: 100 }
            ]},
            { angle: 130, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 50 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.redDark, pos: 0 },
                { color: COLORS.yellow, pos: 45 },
                { color: COLORS.blueDark, pos: 100 }
            ]},
            { angle: 138, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 48 },
                { color: COLORS.blue, pos: 100 }
            ]},
            { angle: 135, stops: [
                { color: COLORS.red, pos: 0 },
                { color: COLORS.yellow, pos: 52 },
                { color: COLORS.blue, pos: 100 }
            ]}
        ][index % GRADIENT_COUNT];
        
        const stops = variation.stops.map(s => 
            `${s.color} ${s.pos}%`
        ).join(', ');
        
        return `linear-gradient(${variation.angle}deg, ${stops})`;
    }
    
    /**
     * Initialize gradient manager
     */
    function init() {
        preloadGradients();
    }
    
    return {
        init,
        getNextGradient,
        applyGradient,
        getCSSGradient,
        GRADIENT_COUNT
    };
})();

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', GradientManager.init);
} else {
    GradientManager.init();
}
