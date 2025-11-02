#!/bin/bash

# ========================================================================
# React Frontend Extraction Script
# ========================================================================
# This script extracts all essential files for the React Pokemon TCG app
# and creates a standalone, deployable package with setup instructions.
#
# Usage: bash extract-react-app.sh
# ========================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "=================================================="
echo "   React Pokemon TCG - Extraction Script"
echo "=================================================="
echo -e "${NC}"

# Prompt for folder name
echo -e "${YELLOW}Enter the folder name for the extracted React app:${NC}"
read -p "Folder name: " FOLDER_NAME

# Validate folder name
if [ -z "$FOLDER_NAME" ]; then
    echo -e "${RED}Error: Folder name cannot be empty${NC}"
    exit 1
fi

# Check if folder already exists
if [ -d "$FOLDER_NAME" ]; then
    echo -e "${YELLOW}Warning: Folder '$FOLDER_NAME' already exists.${NC}"
    read -p "Overwrite? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Extraction cancelled.${NC}"
        exit 1
    fi
    rm -rf "$FOLDER_NAME"
fi

# Create destination folder
echo -e "${GREEN}Creating folder: $FOLDER_NAME${NC}"
mkdir -p "$FOLDER_NAME"

# Copy essential React files
echo -e "${BLUE}Copying React application files...${NC}"

# Root configuration files
echo "  → Configuration files"
cp package.json "$FOLDER_NAME/"
cp vite.config.ts "$FOLDER_NAME/"
cp tailwind.config.js "$FOLDER_NAME/"
cp tsconfig.json "$FOLDER_NAME/"
cp .eslintrc.json "$FOLDER_NAME/" 2>/dev/null || echo "    (no .eslintrc.json found, skipping)"
cp index.html "$FOLDER_NAME/"

# Create README for the extracted app
cat > "$FOLDER_NAME/README.md" << 'EOF'
# Pokemon TCG Search - React App

## Quick Start

### Prerequisites
- Node.js v18+ (tested with v22.21.0)
- npm v9+ (tested with v10.9.4)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app will be available at: http://localhost:8888

### Build for Production

```bash
npm run build
```

Build output will be in the `dist/` folder.

### Testing

```bash
npm run test          # Run tests with watch mode
npm run test:run      # Run tests once
npm run test:ui       # Run tests with UI
```

### Lint

```bash
npm run lint
```

## Project Structure

```
.
├── src/
│   ├── components/      # React components
│   ├── services/        # API services
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── styles/         # Global styles
│   ├── App.tsx         # Root component
│   └── main.tsx        # Entry point
├── public/             # Static assets
├── index.html          # HTML entry point
├── package.json        # Dependencies and scripts
├── vite.config.ts      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
└── tsconfig.json       # TypeScript configuration
```

## Technology Stack

- **React**: 19.2.0 (latest stable)
- **TypeScript**: 5.2.2
- **Vite**: 7.1.12 (build tool)
- **Tailwind CSS**: 4.1.16 (latest stable)
- **Testing**: Vitest 4.0.3

## Features

- Modern React 19 with hooks and concurrent features
- TypeScript for type safety
- Tailwind CSS for styling
- Lazy loading with React.Suspense
- Error boundaries for graceful error handling
- Service worker error handling
- Responsive design
- Accessibility (ARIA labels, semantic HTML)

## API

This app uses the Pokemon TCG API: https://api.pokemontcg.io/v2/cards

## Environment Variables

No environment variables required for basic operation.

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
EOF

# Copy src directory
echo "  → Source files (src/)"
cp -r src "$FOLDER_NAME/"

# Copy public directory if it exists
if [ -d "public" ]; then
    echo "  → Public assets"
    cp -r public "$FOLDER_NAME/"
else
    mkdir -p "$FOLDER_NAME/public"
    echo "    (public folder created)"
fi

# Create a simplified package.json without unnecessary scripts
echo -e "${BLUE}Creating optimized package.json...${NC}"
cat > "$FOLDER_NAME/package.json" << 'EOF'
{
  "name": "pokemon-tcg-search-react",
  "private": true,
  "version": "2.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest",
    "test:run": "vitest run",
    "test:watch": "vitest --watch",
    "test:ui": "vitest --ui"
  },
  "dependencies": {
    "@types/axios": "^0.9.36",
    "axios": "^1.12.2",
    "react": "^19.2.0",
    "react-dom": "^19.2.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.1.16",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.0",
    "@types/react": "^19.2.2",
    "@types/react-dom": "^19.2.2",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "@vitest/ui": "^4.0.3",
    "autoprefixer": "^10.4.21",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "happy-dom": "^20.0.8",
    "postcss": "^8.5.6",
    "tailwindcss": "^4.1.16",
    "typescript": "^5.2.2",
    "vite": "^7.1.12",
    "vitest": "^4.0.3"
  }
}
EOF

# Create setup script
cat > "$FOLDER_NAME/setup.sh" << 'EOF'
#!/bin/bash

# Setup script for React Pokemon TCG Search

echo "=========================================="
echo "  Setting up React Pokemon TCG Search"
echo "=========================================="

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "ERROR: Node.js 18 or higher is required (you have: $(node --version))"
    exit 1
fi

echo "✓ Node.js version: $(node --version)"
echo "✓ npm version: $(npm --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "  Setup Complete!"
    echo "=========================================="
    echo ""
    echo "To start the development server:"
    echo "  npm run dev"
    echo ""
    echo "To build for production:"
    echo "  npm run build"
    echo ""
    echo "To run tests:"
    echo "  npm run test"
    echo ""
else
    echo ""
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
EOF

chmod +x "$FOLDER_NAME/setup.sh"

# Create .gitignore
cat > "$FOLDER_NAME/.gitignore" << 'EOF'
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output/

# Production build
dist/
build/
*.tsbuildinfo

# Development
.vite/
.cache/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*
.pnpm-debug.log*

# Editor
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# OS
Thumbs.db
EOF

# Create extraction summary
echo -e "${GREEN}Creating extraction summary...${NC}"
cat > "$FOLDER_NAME/EXTRACTION_INFO.txt" << EOF
========================================================================
REACT APP EXTRACTION SUMMARY
========================================================================
Extraction Date: $(date)
Source: pokemon-dev repository
Extracted to: $FOLDER_NAME

INCLUDED FILES:
- package.json          (optimized for standalone deployment)
- vite.config.ts        (Vite configuration for port 8888)
- tailwind.config.js    (Tailwind CSS v4.1.16 configuration)
- tsconfig.json         (TypeScript compiler options)
- index.html            (HTML entry point)
- src/                  (Complete React application source)
  - components/         (React components)
  - services/           (API services)
  - types/              (TypeScript definitions)
  - utils/              (Utility functions)
  - styles/             (CSS files)
  - App.tsx             (Root component)
  - main.tsx            (Entry point)
- public/               (Static assets)
- setup.sh              (Automated setup script)
- README.md             (Documentation)
- .gitignore            (Git ignore rules)

SETUP INSTRUCTIONS:
1. cd $FOLDER_NAME
2. bash setup.sh        (or: npm install)
3. npm run dev          (starts dev server on port 8888)

TECHNOLOGY STACK:
- React: 19.2.0 (latest stable as of Nov 2025)
- TypeScript: 5.2.2
- Vite: 7.1.12
- Tailwind CSS: 4.1.16 (latest stable as of Nov 2025)
- Node.js: v18+ required (tested with v22.21.0)

BUILD FOR PRODUCTION:
- npm run build         (creates dist/ folder)
- npm run preview       (preview production build)

EXCLUDED (per requirements):
- node_modules/         (install with npm install)
- .git/                 (version control history)
- dist/                 (build output)
- logs/                 (log files)
- .env files            (environment variables)
- IDE configs           (.vscode, .idea)
- Backend files         (backend/, security-agent/)
- Other frontends       (frontends/port-*/,  hub/, v2/)
- Jekyll files          (_config.yml, Gemfile, index.md)
- Deployment scripts    (deploy-*.sh, watchdog-*.sh)

========================================================================
EOF

# Summary
echo ""
echo -e "${GREEN}=========================================="
echo "  Extraction Complete!"
echo -e "==========================================${NC}"
echo ""
echo "Extracted to: $FOLDER_NAME"
echo ""
echo "Next steps:"
echo -e "  1. ${BLUE}cd $FOLDER_NAME${NC}"
echo -e "  2. ${BLUE}bash setup.sh${NC}    (or: npm install)"
echo -e "  3. ${BLUE}npm run dev${NC}      (start development server)"
echo ""
echo "Files created:"
echo "  ✓ package.json (optimized)"
echo "  ✓ src/ (complete React app)"
echo "  ✓ configuration files (Vite, Tailwind, TypeScript)"
echo "  ✓ setup.sh (automated setup)"
echo "  ✓ README.md (documentation)"
echo "  ✓ EXTRACTION_INFO.txt (summary)"
echo ""
echo -e "${YELLOW}Review EXTRACTION_INFO.txt for complete details.${NC}"
echo ""

# Create a quick reference card
cat > "$FOLDER_NAME/QUICK_REFERENCE.txt" << 'EOF'
QUICK REFERENCE - React Pokemon TCG Search
==========================================

SETUP:
  bash setup.sh

DEVELOPMENT:
  npm run dev              # Start dev server (port 8888)
  npm run build            # Build for production
  npm run preview          # Preview production build

TESTING:
  npm run test             # Run tests (watch mode)
  npm run test:run         # Run tests once
  npm run test:ui          # Run tests with UI

CODE QUALITY:
  npm run lint             # Run ESLint

URLS:
  Development: http://localhost:8888
  API: https://api.pokemontcg.io/v2/cards

BROWSER DEVTOOLS:
  Chrome: F12 or Cmd+Opt+I (Mac)
  Firefox: F12 or Cmd+Opt+I (Mac)

TROUBLESHOOTING:
  - Port 8888 in use? Kill with: npx kill-port 8888
  - Clear cache: rm -rf node_modules/ && npm install
  - Clear Vite cache: rm -rf .vite/
  - TypeScript errors? Check tsconfig.json

DOCS:
  - React: https://react.dev
  - Vite: https://vite.dev
  - Tailwind: https://tailwindcss.com
  - TypeScript: https://www.typescriptlang.org

EOF

echo -e "${GREEN}✓ Extraction completed successfully!${NC}"
echo ""
