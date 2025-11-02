/**
 * Gradient Utilities - Random gradient selection
 * Provides Pokemon-themed gradient options
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

// Define all gradient variations
const GRADIENT_VARIATIONS = [
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
];

/**
 * Get a random gradient from the available options
 */
export function getRandomGradient(): string {
  const randomIndex = Math.floor(Math.random() * GRADIENT_VARIATIONS.length);
  const variation = GRADIENT_VARIATIONS[randomIndex];
  
  const stops = variation.stops.map(s => 
    `${s.color} ${s.pos}%`
  ).join(', ');
  
  return `linear-gradient(${variation.angle}deg, ${stops})`;
}

/**
 * Apply a random gradient to the body element
 */
export function applyRandomGradient(): void {
  const gradient = getRandomGradient();
  if (typeof document !== 'undefined') {
    document.body.style.background = gradient;
    document.body.style.backgroundAttachment = 'fixed';
  }
}
