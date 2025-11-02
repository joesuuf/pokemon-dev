/**
 * Generate 10 animated gradient variations
 * Creates optimized SVG gradients that can be rotated
 */

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

// Create 10 gradient variations with animation-friendly transitions
function generateGradients() {
    const gradients = [];
    
    // Base gradient angles and color positions for smooth animation
    const variations = [
        // Frame 1: Standard diagonal
        { angle: 135, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 50 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 2: Shifted yellow forward
        { angle: 135, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 40 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 3: More yellow, less red
        { angle: 135, stops: [
            { color: COLORS.redLight, pos: 0 },
            { color: COLORS.yellow, pos: 35 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 4: Blue shifted forward
        { angle: 135, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 45 },
            { color: COLORS.blueLight, pos: 90 }
        ]},
        
        // Frame 5: Angle shift slightly
        { angle: 140, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 50 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 6: More vibrant
        { angle: 135, stops: [
            { color: COLORS.redLight, pos: 0 },
            { color: COLORS.yellowLight, pos: 50 },
            { color: COLORS.blueLight, pos: 100 }
        ]},
        
        // Frame 7: Angle shift back
        { angle: 130, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 50 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 8: Yellow dominant
        { angle: 135, stops: [
            { color: COLORS.redDark, pos: 0 },
            { color: COLORS.yellow, pos: 45 },
            { color: COLORS.blueDark, pos: 100 }
        ]},
        
        // Frame 9: Balanced shift
        { angle: 138, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 48 },
            { color: COLORS.blue, pos: 100 }
        ]},
        
        // Frame 10: Return to base with slight variation
        { angle: 135, stops: [
            { color: COLORS.red, pos: 0 },
            { color: COLORS.yellow, pos: 52 },
            { color: COLORS.blue, pos: 100 }
        ]}
    ];
    
    // Generate SVG strings
    variations.forEach((variation, index) => {
        const stops = variation.stops.map(s => 
            `<stop offset="${s.pos}%" stop-color="${s.color}"/>`
        ).join('\n        ');
        
        const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad${index + 1}" x1="0%" y1="0%" x2="100%" y2="100%" gradientUnits="userSpaceOnUse">
      ${stops}
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad${index + 1})"/>
</svg>`;
        
        gradients.push({
            id: index + 1,
            svg: svg,
            angle: variation.angle,
            stops: variation.stops
        });
    });
    
    return gradients;
}

// Export for use in browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { generateGradients, COLORS };
}
