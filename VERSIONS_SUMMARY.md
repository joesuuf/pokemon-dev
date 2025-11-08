# Pokemon TCG Application - Version Summary

## Overview

This document provides a comprehensive overview of all front-end and back-end versions in the Pokemon TCG Search application.

## Front-End Versions

### Total: **7 Front-End Versions**

| Port | Name | Type | Tech Stack | Purpose |
|------|------|------|------------|---------|
| **1111** | Development Hub | React 19 + TypeScript | React 19, Vite 7, TypeScript | Central dashboard for managing all dev servers |
| **4444** | OCR Card Search | React 19 + TypeScript | React 19, GCP Vision API, OCR | Upload images to identify Pokemon cards via OCR |
| **5555** | Main React Frontend | React 18 + TypeScript | React 18, Vite 7, Tailwind CSS 4 | Primary production frontend |
| **6666** | Pure HTML/CSS/JS (v2) | Vanilla JavaScript | Pure HTML/CSS/JS, No frameworks | Zero-dependency static version |
| **7777** | React Variant A | React 18 + TypeScript | React 18, Vite 7, Tailwind CSS 4 | A/B testing variant, experimental features |
| **8888** | React Variant B | React 18 + TypeScript | React 18, Vite 7, Tailwind CSS 4 | Main development server, A/B testing |
| **9999** | React Variant C | React 18 + TypeScript | React 18, Vite 7, Tailwind CSS 4 | Development environment, beta testing |

### Detailed Breakdown

#### Port 1111 - Development Hub
- **Location**: `frontends/port-1111/`
- **Config**: `vite.config.1111.ts`
- **Description**: Central dashboard providing quick access to all running development servers
- **Features**: Server status monitoring, server control interface
- **Start Command**: `npm run hub`

#### Port 4444 - OCR Card Search
- **Location**: `frontends/port-4444/`
- **Config**: `vite.config.4444.ts`
- **Description**: Google Cloud Vision API integration for card identification via image upload
- **Features**: Image upload, OCR processing, card matching
- **Start Command**: `npm run frontend:4444`
- **Backend Integration**: Uses `/api/ocr` routes

#### Port 5555 - Main React Frontend
- **Location**: `frontends/port-5555/`
- **Config**: `vite.config.5555.ts`
- **Description**: Primary Pokemon TCG Search application
- **Features**: 
  - Modern React with TypeScript
  - Tailwind CSS v4 styling
  - Pokemon TCG API integration
  - Grid and List view modes
  - Detailed card modal displays
  - Full test suite
- **Start Command**: `npm run frontend:5555`
- **Tests**: Located in `frontends/port-5555/tests/`

#### Port 6666 - Pure HTML/CSS/JS (v2)
- **Location**: `frontends/port-6666/`
- **Description**: Zero-dependency static version
- **Features**:
  - Pure HTML, CSS, and vanilla JavaScript
  - No build process required
  - Security-focused (XSS protection, CSP)
  - Mobile-first responsive design
  - WCAG 2.1 compliant accessibility
  - Lazy image loading
- **Start Command**: `npm run frontend:6666` (uses http-server)
- **Bundle Size**: ~30KB (vs ~200KB for React versions)

#### Port 7777 - React Variant A
- **Location**: `frontends/port-7777/`
- **Config**: `vite.config.7777.ts`
- **Description**: Alternative React implementation for A/B testing
- **Features**: Same as Port 5555, customizable for experiments
- **Start Command**: `npm run frontend:7777`
- **Tests**: Located in `frontends/port-7777/tests/`

#### Port 8888 - React Variant B (Main Dev Server)
- **Location**: `frontends/port-8888/`
- **Config**: `vite.config.8888.ts`
- **Description**: Main development server with hot module replacement (HMR)
- **Features**: Same as Port 5555, primary development environment
- **Start Command**: `npm run dev` or `npm run frontend:8888`
- **Tests**: Located in `frontends/port-8888/tests/`

#### Port 9999 - React Variant C
- **Location**: `frontends/port-9999/`
- **Config**: `vite.config.9999.ts`
- **Description**: Development environment for experimental features
- **Features**: Same as Port 5555, beta testing environment
- **Start Command**: `npm run frontend:9999`
- **Tests**: Located in `frontends/port-9999/tests/`

## Back-End Versions

### Total: **1 Back-End Version** (with multiple route modules)

#### Backend Server (Port 3001)
- **Location**: `backend/`
- **Description**: Express.js backend server
- **Tech Stack**: 
  - Express.js 4.19.2
  - TypeScript 5.2.2
  - CORS enabled
- **Routes**:
  1. **OCR Routes** (`/api/ocr`)
     - `/api/ocr/upload` - Upload image for OCR processing
     - `/api/ocr/process` - Process OCR using Google Cloud Vision API
     - `/api/ocr/match` - Match OCR results to Pokemon cards
  2. **Server Management Routes** (`/api`)
     - `/api/start-server` - Start a development server
     - `/api/server-status/:port` - Check server status
     - `/api/kill-server/:port` - Kill processes on a port
  3. **Health Check**
     - `/health` - Server health status
- **Start Command**: `cd backend && npm start`
- **Default Port**: 3001 (configurable via `PORT` env var)

## Version Comparison

### React Versions
- **React 19**: Ports 1111, 4444
- **React 18**: Ports 5555, 7777, 8888, 9999

### Framework Types
- **React + TypeScript**: Ports 1111, 4444, 5555, 7777, 8888, 9999
- **Pure HTML/CSS/JS**: Port 6666

### Build Tools
- **Vite 7**: All React versions (ports 1111, 4444, 5555, 7777, 8888, 9999)
- **http-server**: Port 6666 (static files)

### Testing
- **Test Suites Available**: Ports 5555, 7777, 8888, 9999
- **Test Framework**: Vitest 4.0.3
- **Test Libraries**: @testing-library/react, @testing-library/jest-dom

## Running All Versions

### Start All Frontends
```bash
npm run frontends:all
```
This starts all 6 frontend versions simultaneously:
- Port 4444 (OCR)
- Port 5555 (Main React)
- Port 6666 (Pure HTML/JS)
- Port 7777 (React Variant A)
- Port 8888 (React Variant B)
- Port 9999 (React Variant C)

### Start Hub + All Frontends
```bash
npm run start:all
```
This starts:
- Port 1111 (Hub) - Central dashboard
- All frontend versions

### Individual Commands
```bash
npm run hub              # Port 1111
npm run frontend:4444    # Port 4444
npm run frontend:5555    # Port 5555
npm run frontend:6666    # Port 6666
npm run frontend:7777    # Port 7777
npm run dev              # Port 8888 (main dev)
npm run frontend:9999    # Port 9999
```

## Summary Statistics

- **Total Front-End Versions**: 7
- **React Versions**: 6 (React 18: 4, React 19: 2)
- **Vanilla JS Versions**: 1
- **Back-End Versions**: 1 (with 2 route modules)
- **Total Ports Used**: 8 (7 frontend + 1 backend)
- **Test Suites**: 4 (ports 5555, 7777, 8888, 9999)

## Use Cases

1. **Development Hub (1111)**: Central management dashboard
2. **OCR Search (4444)**: Image-based card identification
3. **Main Frontend (5555)**: Primary production application
4. **Static Version (6666)**: Zero-dependency deployment
5. **A/B Testing (7777, 8888, 9999)**: UI experimentation and variant testing
