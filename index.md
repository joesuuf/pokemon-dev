---
layout: default
---

# Pok?mon TCG Search

A standalone React + TypeScript application for searching and displaying Pok?mon Trading Card Game cards.

## Overview

This is a complete, standalone version of the Pok?mon TCG Search application. All essential files have been included to run the application independently.

## Features

### OCR Card Identification
- **Upload card images**: Drag & drop or click to upload Pokemon card images
- **Automatic identification**: Uses Google Cloud Vision API to extract text from card regions
- **95%+ confidence matching**: Matches cards to official Pokemon TCG API with high confidence
- **Real-time processing**: Visual feedback during OCR and matching process
- **Multiple match strategies**: Exact ID, set code + number, or set name matching

### View Modes
- **Card Grid View** (default): Display cards as a clickable grid with images. Click any card to expand and see full details in a modal overlay.
- **Detailed List View**: Display full card information immediately in compact text-based format.

### Search
- Search by Pok?mon name
- Search by attack name
- Combined name + attack search

## Getting Started

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

## Documentation

For more detailed documentation, see:
- [Full README](README.md)
- [GitHub Pages Deployment](GITHUB_PAGES_DEPLOYMENT.md)
- [Security Agent Documentation](security-agent/README.md)
- [Agents Overview](agents/AGENTS_OVERVIEW.md)

## License

This project is part of the Pok?mon TCG Search application suite.

---

**Version**: dev-v0  
**Last Updated**: November 2025  
**Status**: Fully Functional & Ready for Deployment
