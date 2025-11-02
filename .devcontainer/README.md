# Codespaces / DevContainer Configuration

This directory contains the configuration for GitHub Codespaces and VS Code Dev Containers.

## Quick Start

1. **Open in Codespaces:**
   - Go to: https://github.com/joesuuf/pokemon-dev
   - Click: Green "Code" button
   - Select: "Codespaces" tab
   - Click: "Create codespace on main"

2. **Wait for setup (~2-3 minutes):**
   - Container builds automatically
   - Dependencies install (`npm install` + `pip install`)
   - Extensions install
   - Ports auto-forward

3. **Start developing:**
   ```bash
   # React dev server (port 3000)
   npm run dev

   # Main web server (port 8000)
   python3 -m http.server 8000

   # HTML v2 server (port 8080)
   npm run v2:dev
   ```

## What's Configured

### Pre-installed
- Node.js 20
- Python 3.11
- Git
- npm

### VS Code Extensions
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- Python support
- GitHub Copilot (if enabled)

### Port Forwarding
- Port 3000 → React dev server
- Port 8000 → Main web server
- Port 8080 → HTML v2 server

### Auto-Install
- npm dependencies (`npm install`)
- Python dependencies (`pip install -r agents/requirements.txt`)

## Accessing Your Apps

After starting servers, Codespaces will:
1. Auto-forward ports
2. Show notification with public URL
3. Make ports accessible via: `https://<codespace>-3000.app.github.dev`

## Customization

Edit `.devcontainer/devcontainer.json` to:
- Change Node.js version
- Change Python version
- Add more VS Code extensions
- Configure additional ports
- Add custom setup commands
