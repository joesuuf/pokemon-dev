# Frontend Watchdog - Quick Reference

## Status: CONFIGURED & READY ✅

All frontend variant ports are now configured for:
- ✅ **Persistent operation** - Runs continuously in background
- ✅ **Public access** - All ports bind to 0.0.0.0
- ✅ **Auto-restart** - Restarts every 60 seconds
- ✅ **Monitoring** - Built-in status and logging

## Quick Start

```bash
# Start the watchdog (background)
npm run watchdog:start

# Check status
npm run watchdog:status

# Stop the watchdog
npm run watchdog:stop

# View logs
npm run watchdog:logs
```

## Managed Ports

| Port | Type | Public | Auto-Restart |
|------|------|--------|--------------|
| 5555 | Vite | ✅ Yes | ✅ Every 60s |
| 6666 | HTTP Server | ✅ Yes | ✅ Every 60s |
| 7777 | Vite | ✅ Yes | ✅ Every 60s |
| 8888 | Vite | ✅ Yes | ✅ Every 60s |
| 9999 | Vite | ✅ Yes | ✅ Every 60s |

## Files Created

### Scripts
- `watchdog-frontends.sh` - Main watchdog service
- `start-watchdog-background.sh` - Background launcher
- `stop-watchdog.sh` - Stop service
- `status-watchdog.sh` - Check status

### Documentation
- `WATCHDOG.md` - Complete documentation
- `WATCHDOG_SUMMARY.md` - This quick reference

### Package.json Updates
- Added `npm-run-all` dependency
- Updated `frontend:6666` to bind to 0.0.0.0
- Added watchdog commands:
  - `npm run watchdog`
  - `npm run watchdog:start`
  - `npm run watchdog:stop`
  - `npm run watchdog:status`
  - `npm run watchdog:logs`

## Configuration Details

### Vite Configs (5555, 7777, 8888, 9999)
```typescript
server: {
  port: <PORT>,
  strictPort: true,
  host: true  // Binds to 0.0.0.0
}
```

### HTTP Server (6666)
```bash
npx http-server frontends/port-6666 -p 6666 -a 0.0.0.0 --cors
```

## Access URLs

### Local
```
http://localhost:5555
http://localhost:6666
http://localhost:7777
http://localhost:8888
http://localhost:9999
```

### Remote (if accessible)
```
http://<your-ip>:5555
http://<your-ip>:6666
http://<your-ip>:7777
http://<your-ip>:8888
http://<your-ip>:9999
```

### GitHub Codespaces
```
https://<codespace>-5555.app.github.dev
https://<codespace>-6666.app.github.dev
https://<codespace>-7777.app.github.dev
https://<codespace>-8888.app.github.dev
https://<codespace>-9999.app.github.dev
```

## How It Works

1. **Start**: Watchdog launches all 5 frontend servers
2. **Monitor**: Runs for 60 seconds
3. **Restart**: Kills and restarts all servers
4. **Repeat**: Continues indefinitely

### Benefits
- No memory leaks
- Fresh processes every minute
- Auto-recovery from hangs
- Maximum uptime

## Logs Location

```
logs/watchdog/
├── watchdog.log              # Main watchdog log
├── watchdog-background.log   # Background process log
├── watchdog.pid              # Process ID file
├── port-5555.log            # Port 5555 output
├── port-6666.log            # Port 6666 output
├── port-7777.log            # Port 7777 output
├── port-8888.log            # Port 8888 output
└── port-9999.log            # Port 9999 output
```

## Verification Checklist

- [x] All 5 ports configured for public access (0.0.0.0)
- [x] Watchdog script with 60-second restart cycle
- [x] Background start/stop scripts
- [x] Status monitoring script
- [x] NPM commands for easy management
- [x] Comprehensive documentation
- [x] Logging system
- [x] Auto-dependency installation
- [x] Graceful shutdown handling

## Next Steps

1. **Install dependencies** (if not already done):
   ```bash
   npm install
   ```

2. **Start the watchdog**:
   ```bash
   npm run watchdog:start
   ```

3. **Verify all ports are running**:
   ```bash
   npm run watchdog:status
   ```

4. **Access the frontends** via the URLs above

## Troubleshooting

### Issue: Watchdog won't start
```bash
npm run watchdog:stop
npm run watchdog:start
```

### Issue: Ports already in use
```bash
npm run watchdog:stop
# Wait a few seconds
npm run watchdog:start
```

### Issue: Dependencies missing
```bash
npm install
```

## For More Information

See [WATCHDOG.md](WATCHDOG.md) for complete documentation including:
- Advanced configuration
- Production deployment
- Security considerations
- Performance optimization
- Detailed troubleshooting
