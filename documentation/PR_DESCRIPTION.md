feat(hub): Convert to React/TS with server management

## Summary

Converted `hub/index.html` from static HTML to a React/TypeScript application with full server management capabilities.

## Changes

- **Frontend**: Complete React/TS rewrite of hub dashboard
  - Real-time server status monitoring (checks every 10s)
  - Start/kill server controls with UI feedback
  - Visual status indicators for all 6 development servers

- **Backend**: Enhanced server management API
  - Added `/api/kill-server/:port` endpoint
  - Auto-kill duplicate processes before starting servers
  - Cross-platform process management (Linux/Mac/Windows)

## Features

? Detect server state for ports 4444, 6666, 7777, 8888, 9999, 1111  
? Start servers with automatic duplicate cleanup  
? Kill servers via API  
? Real-time status updates  

## Technical Details

- React 19.2.0 + TypeScript + Vite
- Backend uses `lsof`/`netstat` for process detection
- Graceful shutdown before force kill
- Proper error handling and user feedback
