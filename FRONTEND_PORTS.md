# Front-End Port Configuration

All three front-ends are configured to run on persistent ports and are publicly accessible (0.0.0.0).

## Port Configuration

- **React Front-End**: Port `8888` (Vite dev server)
- **HTML Front-End (v2)**: Port `9999` (HTTP server)
- **Carousel Front-End**: Port `7777` (HTTP server)

All servers are configured with `host: 0.0.0.0` for public/remote access.

## Quick Start Commands

### Start All Three Front-Ends (Recommended)

```bash
# Install dependencies first
npm install

# Start all three servers simultaneously
npm run start:all
```

Or use the convenience scripts:

```bash
# Linux/WSL/Bash
npm run dev:all

# Windows PowerShell
npm run dev:all:win
```

### Start Individual Front-Ends

```bash
# React Front-End (Port 8888)
npm run dev

# HTML Front-End (Port 9999)
npm run v2:serve

# Carousel Front-End (Port 7777)
npm run carousel:serve
```

## Access URLs

Once started, access the front-ends at:

- **React**: http://localhost:8888 or http://0.0.0.0:8888
- **HTML v2**: http://localhost:9999 or http://0.0.0.0:9999
- **Carousel**: http://localhost:7777 or http://0.0.0.0:7777

### Remote Access (Codespaces/WSL)

For GitHub Codespaces, access via:
- React: `https://<codespace-name>-8888.app.github.dev`
- HTML v2: `https://<codespace-name>-9999.app.github.dev`
- Carousel: `https://<codespace-name>-7777.app.github.dev`

For local network access:
- React: `http://<your-ip>:8888`
- HTML v2: `http://<your-ip>:9999`
- Carousel: `http://<your-ip>:7777`

## Persistent Configuration Files

### React Front-End (Port 8888)
- **File**: `vite.config.ts`
- **Configuration**: 
  ```typescript
  server: {
    port: 8888,
    host: '0.0.0.0'
  }
  ```

### HTML Front-End (Port 9999)
- **File**: `package.json`
- **Scripts**:
  - `v2:dev`: Python HTTP server on port 9999
  - `v2:serve`: Node.js http-server on port 9999

### Carousel Front-End (Port 7777)
- **File**: `package.json`
- **Scripts**:
  - `carousel:dev`: Python HTTP server on port 7777
  - `carousel:serve`: Node.js http-server on port 7777
- **Location**: `carousel/index.html`

## One-Liner Commands

### PowerShell (Windows)
```powershell
npm install; npm run start:all
```

### Bash (Linux/WSL)
```bash
npm install && npm run start:all
```

## Verification

To verify all servers are running:

```bash
# Check ports
netstat -an | findstr "8888 9999 7777"    # Windows
netstat -an | grep "8888\|9999\|7777"     # Linux/WSL
```

Or visit each URL in your browser:
- http://localhost:8888
- http://localhost:9999
- http://localhost:7777

## Troubleshooting

### Port Already in Use
If a port is already in use, you can:
1. Stop the process using the port
2. Or change the port in the configuration files

### Dependencies Not Installed
Run `npm install` to install all required dependencies including:
- `concurrently` - For running multiple servers
- `http-server` - For serving static HTML files

### Python vs Node.js
Both Python (`python -m http.server`) and Node.js (`npx http-server`) options are available. The scripts will use whichever is available.

