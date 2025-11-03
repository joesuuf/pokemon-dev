# Front-End Port Configuration

All three front-ends are configured to run on persistent ports and are publicly accessible (0.0.0.0).

## Port Configuration
- **Development Hub**: Port `1111` (Vite dev server)
- **OCR Search Front-End**: Port `4444` (Vite dev server)
- **Pure HTML Front-End**: Port `6666` (http-server)
- **React Variants**: Ports `5555`, `7777`, `8888`, `9999` (Vite)
- **HTML Front-End (v2)**: Port `9999` (HTTP server)
- **Carousel Front-End**: Port `7777` (HTTP server)
- **Development Hub**: Port `1111` (HTTP server)
- **Backend API**: Port `3001` (Express server)

All servers are configured with `host: 0.0.0.0` for public/remote access.

## Quick Start Commands
```bash
npm run hub
```
```bash
npm run frontends:all
```

### Start Individual Front-Ends
```bash
npm run frontend:4444
```
```bash
npm run frontend:6666
```
```bash
npm run frontend:8888
```
```bash
npm run frontend:9999
```
```bash
npm run frontend:7777
```
## Access URLs
- **HTML**: http://localhost:6666
- **Carousel**: http://localhost:6666/carousel

