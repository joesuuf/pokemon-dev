# Pokémon TCG Search - Dev v0

A standalone React + TypeScript application for searching and displaying Pokémon Trading Card Game cards.

## 📋 Overview

This is a complete, standalone version of the Pokémon TCG Search application. All essential files have been included to run the application independently.

## 🗂️ Project Structure

```
pokemon-dev/
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
├── agents/                       # Modular agent framework
│   ├── python/                   # Python agents
│   │   └── security_agent_v2.py  # Security scanning agent v2
│   ├── md/                       # Agent configurations
│   └── workflows/                # Agent workflows
├── security-agent/               # Security scanning (v2 primary)
│   ├── v1/                       # ⚠️ ARCHIVED - Do not use
│   ├── config/                   # Agent configurations
│   ├── reports/                  # Generated security reports
│   └── README.md                 # Security agent documentation
├── v2/                           # V2 static application
│   ├── index.html                # V2 app entry
│   ├── scripts/                  # V2 JavaScript
│   └── styles/                   # V2 CSS
├── carousel/                     # Standalone carousel component
│   └── index.html                # Carousel demo
├── hub/                          # Development hub (NEW)
│   └── index.html                # Central dashboard on port 1111
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

**Quick Start - All Servers:**
```bash
npm run start:all
```
This launches all development servers concurrently:
- Main app (Vite) on port 5173
- V2 app (static) on port 9999
- Carousel on port 7777
- Development hub on port 1111

**Individual Servers:**
```bash
npm run dev          # Main development server (port 5173)
npm run dev:6666     # Alternate dev server (port 6666)
npm run frontend:4444 # OCR Card Search (port 4444)
npm run v2           # V2 static app (port 9999)
npm run carousel     # Carousel component (port 7777)
npm run hub          # Development hub (port 1111)
npm run backend      # Backend API server (port 3001)
```

**🎯 Development Hub:** Open `http://localhost:1111` for a central dashboard with links to all running servers and documentation.

**Advanced:** Run all servers including alternate port:
```bash
npm run start:all+6666  # Runs 5 servers total
```

**Watchdog Service (Auto-restart):**
```bash
npm run watchdog:start  # Start watchdog to keep all servers running
npm run watchdog:stop   # Stop watchdog
npm run watchdog:status # Check status
npm run watchdog:logs   # View logs
```
The watchdog automatically restarts frontend servers on ports 4444, 5555, 6666, 7777, 8888, and 9999 every 60 seconds for maximum reliability.

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

### Security Scanning

Run comprehensive security scan with v2 agent:
```bash
npm run security:scan        # Full security scan
npm run security:report      # Generate JSON report
npm run security:ci          # CI/CD integration (fails on critical issues)
```

The security agent scans for:
- XSS, CSRF, CORS vulnerabilities
- Dependency vulnerabilities
- OWASP Top 10 compliance
- Performance security issues
- Mobile security concerns
- Dead code detection

See `agents/python/security_agent_v2.py` for details.

## ✨ Features

### OCR Card Identification (NEW!)
- **Upload card images**: Drag & drop or click to upload Pokemon card images
- **Automatic identification**: Uses Google Cloud Vision API to extract text from card regions
- **95%+ confidence matching**: Matches cards to official Pokemon TCG API with high confidence
- **Real-time processing**: Visual feedback during OCR and matching process
- **Multiple match strategies**: Exact ID, set code + number, or set name matching
- Access at: `http://localhost:4444`

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

## 🌐 Development Servers

This project runs multiple development servers for different purposes:

| Port | Server | Purpose | Technology |
|------|--------|---------|------------|
| **1111** | Development Hub | Central dashboard with links to all servers | http-server |
| **3001** | Backend API | OCR and card matching API server | Express/Node.js |
| **4444** | OCR Search | Card identification via image upload | Vite/React |
| **5173** | Main App | Primary development server with HMR | Vite |
| **6666** | Alt App | Alternate instance for A/B testing | Vite |
| **7777** | Carousel | Standalone component demo | http-server |
| **9999** | V2 App | Static production-like build | http-server |

### Server Features

**Vite Servers (5173, 6666):**
- Hot Module Replacement (HMR)
- Live TypeScript compilation
- React Fast Refresh
- Development debugging tools

**http-server Instances (1111, 7777, 9999):**
- CORS enabled for API testing
- Cache disabled (-c-1) for fresh content
- Dotfiles hidden for security
- Auto-opens browser on start

### Why Multiple Servers?

- **Port 1111 (Hub):** Quick access to all servers and documentation
- **Port 3001 (Backend):** Express API server for OCR processing and card matching
- **Port 4444 (OCR):** Card identification feature with Google Vision API integration
- **Port 5173 (Main):** Primary development with hot reload
- **Port 6666 (Alt):** Test multiple versions or branches simultaneously
- **Port 7777 (Carousel):** Component isolation and integration testing
- **Port 9999 (V2):** Production-like static serving for final testing

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

### Pokémon TCG API
The application connects to the **Pokémon TCG API v2**:
- Endpoint: `https://api.pokemontcg.io/v2/cards`
- Query syntax: `name:*query*` for card names, `attacks.name:*query*` for attack names
- Timeout: 60 seconds per request

### Google Cloud Vision API (OCR)
- **Service**: Google Cloud Vision API for text extraction
- **Backend**: Express server on port 3001
- **Authentication**: Uses `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- **Endpoints**:
  - `POST /api/ocr/upload` - Upload card image
  - `POST /api/ocr/process` - Extract text via OCR
  - `POST /api/ocr/match` - Match extracted text to Pokemon cards
- **Setup**: See `docs/OCR_GOOGLE_CLOUD_SETUP.md` for configuration

## 📝 Environment Variables

Create a `.env` file based on `env.example`:

### Frontend
```
VITE_API_TIMEOUT=60000
VITE_OCR_API_URL=http://localhost:3001  # Backend API URL for OCR
```

### Backend (for OCR feature)
```bash
# Google Cloud Vision API
GOOGLE_APPLICATION_CREDENTIALS=./gcp-key.json

# Pokemon TCG API
POKEMON_TCG_API_KEY=your-pokemon-tcg-api-key

# Server Configuration
PORT=3001
CORS_ORIGIN=http://localhost:4444
```

See `backend/.env.example` for backend configuration template.

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
