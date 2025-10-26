# Pokémon TCG Search - Dev v0

A standalone React + TypeScript application for searching and displaying Pokémon Trading Card Game cards.

## 📋 Overview

This is a complete, standalone version of the Pokémon TCG Search application. All essential files have been included to run the application independently.

## 🗂️ Project Structure

```
pokemon-dev-v0/
├── src/                          # Source code
│   ├── components/               # React components
│   │   ├── CardDisplay.tsx       # Detailed 3-column card view
│   │   ├── CardList.tsx          # Card list container with view modes
│   │   ├── GridCardItem.tsx      # Card grid item with modal
│   │   ├── SearchForm.tsx        # Search form with view mode selector
│   │   ├── LoadingSpinner.tsx    # Loading spinner with countdown timer
│   │   ├── ErrorMessage.tsx      # Error message display
│   │   └── ...other components
│   ├── services/                 # API services
│   │   └── pokemonTcgApi.ts      # Pokémon TCG API client (60s timeout)
│   ├── types/                    # TypeScript types
│   │   └── pokemon.ts            # Card and search types
│   ├── styles/                   # Global and component styles
│   │   └── App.css               # 3-column layout CSS + Pokemon theme
│   ├── utils/                    # Utility functions
│   ├── tests/                    # Unit tests
│   ├── App.tsx                   # Root component
│   ├── main.tsx                  # React entry point
│   └── index.css                 # Global styles
├── api/                          # Serverless API functions
│   └── cards.ts                  # Card API endpoint
├── public/                       # Static assets
├── package.json                  # Dependencies and scripts
├── tsconfig.json                 # TypeScript configuration
├── vite.config.ts                # Vite bundler config
├── vitest.config.ts              # Vitest config
├── index.html                    # HTML entry point
├── env.example                   # Environment variables template
└── README.md                     # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm 9+

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Create environment file (optional):**
   ```bash
   cp env.example .env
   ```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000/`

### Building

Create a production build:
```bash
npm run build
```

### Testing

Run unit tests:
```bash
npm run test
```

Run tests in watch mode:
```bash
npm run test:watch
```

## ✨ Features

### View Modes
- **Card Grid View** (default): Display cards as a clickable grid with images. Click any card to expand and see full details in a modal overlay.
- **Detailed List View**: Display full card information immediately in compact text-based format.

### Search
- Search by Pokémon name
- Search by attack name
- Combined name + attack search

### Search UI
- 60-second countdown timer displayed in spinner's pokéball center
- Real-time timer showing remaining search time
- Live timer updates during API request

### 3-Column Detailed Layout
When viewing detailed card information:
- **Column 1**: Large card image (best quality) + basic specs (HP, Types, Subtypes, Rarity)
- **Column 2**: Set information (name, series, number, artist, release date) + TCGPlayer pricing
- **Column 3**: Scrollable section with abilities, attacks, weaknesses, resistances, retreat cost, and flavor text

### Responsive Design
- Fully responsive on desktop, tablet, and mobile
- 1200px breakpoint: 2-column layout with Column 3 spanning full width
- 768px breakpoint: Single-column layout for mobile

### Pokemon Theme Colors
- Red: #CC0000 (Primary accent)
- Yellow: #FFDE00 (Secondary accent)
- Blue: #003DA5 (Tertiary accent)

## 🔧 Configuration Files

### TypeScript Configuration (`tsconfig.json`)
- Targets ES2020
- Strict type checking enabled
- JSX support for React

### Vite Configuration (`vite.config.ts`)
- React Fast Refresh for hot module reloading
- Automatic React plugin
- 60-second API timeout configured

### Vitest Configuration (`vitest.config.ts`)
- Vitest test runner with React testing library
- DOM environment for component testing

## 📦 Dependencies

Key dependencies:
- **react** - UI framework
- **react-dom** - React DOM rendering
- **typescript** - Type safety
- **vite** - Fast build tool
- **axios** - HTTP client
- **tailwindcss** - Utility-first CSS framework
- **vitest** - Unit testing framework
- **@testing-library/react** - React component testing

Run `npm list` for complete dependency tree.

## 🌐 API Integration

The application connects to the **Pokémon TCG API v2**:
- Endpoint: `https://api.pokemontcg.io/v2/cards`
- Query syntax: `name:*query*` for card names, `attacks.name:*query*` for attack names
- Timeout: 60 seconds per request

## 📝 Environment Variables

Create a `.env` file based on `env.example`:
```
VITE_API_TIMEOUT=60000
```

## 🧪 Testing

Unit tests are located in `src/tests/` and cover:
- Component rendering and props
- API service functionality
- TypeScript type definitions

## 📦 Production Deployment

### Vercel
Configuration is included in `vercel.json` for automatic deployment to Vercel.

### Build & Serve Locally
```bash
npm run build
npm run preview
```

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is already in use, Vite will automatically use the next available port.

### API Timeout
If searches are timing out:
1. Check your internet connection
2. Try a simpler search query
3. Wait a moment and try again

### Module Not Found Errors
If you get module errors after cloning:
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📄 File Manifest

### Root-Level Files Included
- `package.json` - Dependencies and npm scripts
- `package-lock.json` - Locked dependency versions for reproducible builds
- `tsconfig.json` - TypeScript configuration
- `tsconfig.node.json` - TypeScript config for build tools
- `vite.config.ts` - Vite bundler configuration
- `vitest.config.ts` - Vitest test runner configuration
- `postcss.config.js` - PostCSS configuration
- `tailwind.config.js` - Tailwind CSS configuration
- `index.html` - HTML entry point
- `.eslintrc.json` - ESLint linting rules
- `.gitignore` - Git ignore patterns
- `env.example` - Environment variables template
- `index.js` - Node.js entry point
- `vercel.json` - Vercel deployment config
- `error-blank.png` - Asset used in error states

### Directories Included
- `src/` - All source code (29 files)
  - Components, services, types, utils, tests, styles
- `api/` - Serverless API function
  - `cards.ts` - Card lookup endpoint

### NOT Included (Can be regenerated)
- `node_modules/` - Will be installed with `npm install`
- `dist/` - Build output (generated with `npm run build`)
- `documentation/` - Internal development notes
- `.claude/` - Claude Code configuration
- `.env` - Sensitive environment variables
- Test scripts (`test-*.js`) - Development aids

## 📊 Stats

- **Total Source Files**: 29+ files in src/
- **Components**: 15+ React components
- **Tests**: 5+ test suites
- **CSS**: 3000+ lines of Pokemon-themed styling
- **Size**: ~30MB with node_modules (includes all dependencies)
- **Build Size**: ~200KB minified + gzipped

## 🎮 Usage Examples

### Search by Pokémon Name
1. Enter "Charizard" in the search field
2. Select "Card Grid View" to see cards as tiles
3. Click any card to see full details

### Search by Attack
1. Enter "push" in the search field (when using SearchForm+Attack)
2. View results in either grid or detailed view
3. See attack details in Column 3

### View Modes Toggle
- Click "Card Grid View" radio button for tile-based browsing
- Click "Detailed List View" radio button for comprehensive text display
- Switch between views without re-searching

## 🔐 Security

- No sensitive data stored in repository
- Environment variables defined in `.env` (not in version control)
- API keys/tokens should be added to `.env`

## 📄 License

This project is part of the Pokémon TCG Search application suite.

## 🤝 Support

For issues or questions, refer to the documentation in the parent project.

---

**Version**: dev-v0
**Last Updated**: October 25, 2025
**Status**: Fully Functional & Ready for Deployment
