# Update Dashboard for External Access and Server Start

## ?? Overview
This PR enhances the Central Dashboard (`hub/index.html`) to support mobile access and provides live server status monitoring with the ability to start servers remotely.

## ? Features

### 1. Public URL Detection
- Automatically detects hostname/IP when accessed
- Dynamically updates all server links to use public URLs instead of `localhost`
- Enables mobile device access when dashboard is accessed via IP address
- Works seamlessly with Codespaces, WSL, and local network access

### 2. Live Server Status Monitoring
- **Real-time status checks** using actual fetch requests (not simulated)
- Checks all 6 development servers:
  - Port 4444: OCR Search
  - Port 6666: Alternate Dev Server
  - Port 7777: Carousel Component
  - Port 8888: Main Development Server
  - Port 9999: V2 Application
  - Port 1111: Development Hub
- Visual status indicators (green for running, red for stopped)
- Auto-refreshes every 10 seconds
- Uses `no-cors` mode to handle CORS restrictions gracefully

### 3. Server Start Functionality
- **"Start Server" buttons** appear automatically when servers are not running
- Backend API endpoint (`POST /api/start-server`) to programmatically start servers
- Fallback instructions displayed if backend API is unavailable
- Correct port mappings configured (fixed port 5173 ? 8888)

### 4. Backend API Integration
- New `backend/routes/servers.ts` with server management endpoints:
  - `POST /api/start-server` - Starts a development server
  - `GET /api/server-status/:port` - Checks if a server is running
- Integrated into main backend server (`backend/server.ts`)

## ?? Technical Changes

### Files Modified
- `hub/index.html` - Enhanced dashboard with public URL detection, live status, and start buttons
- `backend/server.ts` - Added server routes integration
- `backend/routes/servers.ts` - **New file** with server management API

### Key Implementation Details
- **Hostname Detection**: Uses `window.location.hostname` to detect current access method
- **Status Checking**: Uses fetch with `no-cors` mode to avoid CORS issues while detecting server availability
- **Server Starting**: Uses Node.js `spawn` to start npm scripts in detached processes
- **URL Updates**: Dynamically updates all server links on page load

## ?? Mobile Access
When accessing the dashboard via IP address (e.g., `http://192.168.1.100:1111`), all server links automatically use the same IP address, enabling seamless mobile device access.

## ?? Testing
- ? Dashboard accessible via localhost
- ? Dashboard accessible via IP address
- ? Server status correctly detects running/stopped servers
- ? Start buttons appear when servers are down
- ? URLs update dynamically based on access method

## ?? Usage

### Access Dashboard
```bash
# Start hub server
npm run hub

# Access via:
# - Localhost: http://localhost:1111
# - Network IP: http://<your-ip>:1111
# - Mobile: http://<your-ip>:1111 (on same network)
```

### Start Servers via Dashboard
1. Open dashboard in browser
2. If a server shows "Not Running", click "Start Server" button
3. Server will start automatically (requires backend API running)

### Start Servers via Backend API
```bash
# Start backend first
npm run backend

# Start a server via API
curl -X POST http://localhost:3001/api/start-server \
  -H "Content-Type: application/json" \
  -d '{"port": 8888, "script": "dev"}'
```

## ?? Checklist
- [x] Public URL detection implemented
- [x] Live server status checking (not simulated)
- [x] Server start buttons added
- [x] Backend API endpoints created
- [x] Port numbers corrected (8888 instead of 5173)
- [x] Mobile access support verified
- [x] CORS handling for status checks
- [x] Error handling and fallbacks

## ?? Related
- Addresses mobile access requirements
- Improves developer workflow with one-click server starting
- Enhances dashboard usability with live status updates
