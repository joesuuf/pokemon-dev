# Frontend Watchdog Service

## Overview

The Frontend Watchdog Service ensures all frontend variant ports are **persistent**, **public**, and **always running**. It includes an automatic restart mechanism that cycles all ports every 60 seconds for maximum reliability.

## Features

- **Persistent Operation**: Runs continuously in the background
- **Public Access**: All ports bind to `0.0.0.0` for external access
- **Auto-Restart**: Automatically restarts all ports every 60 seconds
- **Health Monitoring**: Built-in status checking and logging
- **Clean Shutdown**: Graceful cleanup of all processes and ports
- **Multiple Ports**: Manages 5 frontend variants simultaneously

## Port Configuration

All frontend variants are configured for public access and persistent operation:

| Port | Type | Configuration | Public Access |
|------|------|---------------|---------------|
| 5555 | Vite | `vite.config.5555.ts` | ✅ Yes (`host: true`) |
| 6666 | HTTP Server | http-server with `-a 0.0.0.0` | ✅ Yes |
| 7777 | Vite | `vite.config.7777.ts` | ✅ Yes (`host: true`) |
| 8888 | Vite | `vite.config.8888.ts` | ✅ Yes (`host: true`) |
| 9999 | Vite | `vite.config.9999.ts` | ✅ Yes (`host: true`) |

### Vite Configuration

All Vite-based frontends (5555, 7777, 8888, 9999) use this configuration:

```typescript
server: {
  port: <PORT_NUMBER>,
  strictPort: true,  // Ensures exact port is used
  host: true        // Binds to 0.0.0.0 for public access
}
```

### HTTP Server Configuration

Port 6666 uses http-server with public binding:

```bash
npx http-server frontends/port-6666 -p 6666 -a 0.0.0.0 --cors
```

## Quick Start

### Start the Watchdog (Background Mode)

```bash
npm run watchdog:start
```

This will:
- Start the watchdog service in the background
- Launch all 5 frontend ports
- Restart them every 60 seconds
- Create log files in `logs/watchdog/`

### Check Status

```bash
npm run watchdog:status
```

Shows:
- Watchdog process status and PID
- Status of each frontend port
- Access URLs

### Stop the Watchdog

```bash
npm run watchdog:stop
```

This will:
- Gracefully stop the watchdog service
- Clean up all frontend ports
- Remove PID files

### View Logs

```bash
npm run watchdog:logs
```

Tails the watchdog log file in real-time.

## Commands Reference

### NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run watchdog` | Run watchdog in foreground (interactive) |
| `npm run watchdog:start` | Start watchdog in background |
| `npm run watchdog:stop` | Stop watchdog and all ports |
| `npm run watchdog:status` | Show status of watchdog and ports |
| `npm run watchdog:logs` | View watchdog logs (tail -f) |

### Direct Script Execution

```bash
# Start in foreground (with terminal output)
./watchdog-frontends.sh

# Start in background
./start-watchdog-background.sh

# Stop watchdog
./stop-watchdog.sh

# Check status
./status-watchdog.sh
```

## File Structure

```
pokemon-dev/
├── watchdog-frontends.sh           # Main watchdog service script
├── start-watchdog-background.sh    # Background launcher
├── stop-watchdog.sh                # Cleanup script
├── status-watchdog.sh              # Status checker
├── logs/
│   └── watchdog/
│       ├── watchdog.log            # Main watchdog log
│       ├── watchdog-background.log # Background process log
│       ├── watchdog.pid            # Process ID file
│       ├── port-5555.log          # Port 5555 output
│       ├── port-6666.log          # Port 6666 output
│       ├── port-7777.log          # Port 7777 output
│       ├── port-8888.log          # Port 8888 output
│       └── port-9999.log          # Port 9999 output
└── frontends/
    ├── port-5555/
    ├── port-6666/
    ├── port-7777/
    ├── port-8888/
    └── port-9999/
```

## How It Works

### Watchdog Loop

1. **Initial Start**: Starts all 5 frontend ports
2. **Monitor**: Waits 60 seconds
3. **Restart**: Kills all ports and restarts them
4. **Repeat**: Continues loop indefinitely

### Port Management

For each port, the watchdog:

1. **Kill**: Terminates any existing process on the port
2. **Wait**: Allows 1 second for port to be released
3. **Start**: Launches the appropriate server (Vite or HTTP)
4. **Verify**: Checks that the port is listening
5. **Log**: Records the status and PID

### Restart Mechanism

Every 60 seconds:
- All ports are terminated cleanly
- Ports are released from the system
- Fresh server processes are started
- Status is verified and logged

This ensures:
- No memory leaks accumulate
- Configuration changes are picked up
- Hung processes are recovered
- Maximum uptime and reliability

## Access URLs

### Local Access

```
http://localhost:5555
http://localhost:6666
http://localhost:7777
http://localhost:8888
http://localhost:9999
```

### Remote Access

Since all ports bind to `0.0.0.0`, they're accessible remotely:

#### Network Access
```
http://<your-ip>:5555
http://<your-ip>:6666
http://<your-ip>:7777
http://<your-ip>:8888
http://<your-ip>:9999
```

#### GitHub Codespaces
```
https://<codespace-name>-5555.app.github.dev
https://<codespace-name>-6666.app.github.dev
https://<codespace-name>-7777.app.github.dev
https://<codespace-name>-8888.app.github.dev
https://<codespace-name>-9999.app.github.dev
```

## Troubleshooting

### Watchdog Won't Start

**Issue**: "Watchdog is already running"

**Solution**:
```bash
# Check status
npm run watchdog:status

# Stop existing instance
npm run watchdog:stop

# Start fresh
npm run watchdog:start
```

### Port Already in Use

**Issue**: Port conflicts with existing process

**Solution**: The watchdog automatically kills processes on managed ports. If issues persist:

```bash
# Manual cleanup
for port in 5555 6666 7777 8888 9999; do
    lsof -ti :$port | xargs kill -9 2>/dev/null || true
done

# Restart watchdog
npm run watchdog:stop
npm run watchdog:start
```

### Missing Dependencies

**Issue**: `npm-run-all` or `http-server` not found

**Solution**:
```bash
npm install
```

### Logs Not Appearing

**Issue**: Log files not created

**Solution**: The watchdog creates the `logs/watchdog/` directory automatically. If logs are missing, check file permissions:

```bash
ls -la logs/watchdog/
```

### Processes Not Restarting

**Issue**: Watchdog runs but ports stay down

**Solution**: Check individual port logs:

```bash
cat logs/watchdog/port-5555.log
cat logs/watchdog/port-6666.log
# etc.
```

## Advanced Configuration

### Adjust Restart Interval

Edit `watchdog-frontends.sh`:

```bash
RESTART_INTERVAL=60  # Change to desired seconds
```

Default is 60 seconds (1 minute). You can set:
- `30` for 30-second restarts
- `120` for 2-minute restarts
- `300` for 5-minute restarts

### Modify Port List

Edit `watchdog-frontends.sh`:

```bash
PORTS=(5555 6666 7777 8888 9999)  # Add or remove ports
```

### Change Log Directory

Edit `watchdog-frontends.sh`:

```bash
LOG_DIR="logs/watchdog"  # Change to desired path
```

## Production Deployment

### Using systemd (Linux)

Create a systemd service for automatic startup:

```bash
sudo nano /etc/systemd/system/frontend-watchdog.service
```

```ini
[Unit]
Description=Frontend Watchdog Service
After=network.target

[Service]
Type=forking
User=<your-user>
WorkingDirectory=/path/to/pokemon-dev
ExecStart=/path/to/pokemon-dev/start-watchdog-background.sh
ExecStop=/path/to/pokemon-dev/stop-watchdog.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable frontend-watchdog
sudo systemctl start frontend-watchdog
sudo systemctl status frontend-watchdog
```

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Start with PM2
pm2 start watchdog-frontends.sh --name frontend-watchdog

# Save configuration
pm2 save

# Auto-start on boot
pm2 startup
```

## Monitoring and Alerts

### Real-time Monitoring

```bash
# Watch logs continuously
npm run watchdog:logs

# Or use multitail for all logs
multitail logs/watchdog/*.log
```

### Status Checking Script

Create a cron job to periodically check status:

```bash
# Edit crontab
crontab -e

# Add this line (check every 5 minutes)
*/5 * * * * cd /path/to/pokemon-dev && npm run watchdog:status >> logs/watchdog/cron-status.log 2>&1
```

## Performance Considerations

### Resource Usage

Each frontend port consumes:
- **Memory**: ~50-100MB per Vite instance
- **CPU**: Minimal when idle, 5-10% during restarts
- **Network**: Varies by traffic

Total for all 5 ports:
- **Memory**: ~300-500MB
- **CPU**: ~2-5% average
- **Disk**: Logs grow ~1-5MB per day

### Optimization Tips

1. **Adjust restart interval** based on your needs
2. **Use log rotation** to prevent disk filling
3. **Monitor system resources** during peak usage
4. **Consider disabling ports** you don't actively use

### Log Rotation

Add to `/etc/logrotate.d/frontend-watchdog`:

```
/path/to/pokemon-dev/logs/watchdog/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
```

## Security Considerations

### Public Binding

All ports bind to `0.0.0.0`, making them accessible from:
- Local network
- Internet (if firewall allows)
- GitHub Codespaces forwarding

### Recommendations

1. **Use HTTPS** in production (reverse proxy with nginx/caddy)
2. **Configure firewall** to restrict access
3. **Implement authentication** if serving sensitive data
4. **Regular updates** of dependencies

### Firewall Configuration

```bash
# Allow only local network (example: 192.168.1.0/24)
sudo ufw allow from 192.168.1.0/24 to any port 5555:9999 proto tcp

# Or allow specific IPs
sudo ufw allow from <trusted-ip> to any port 5555:9999 proto tcp
```

## FAQ

### Q: Why restart every minute?

**A**: Frequent restarts ensure:
- No memory leaks accumulate
- Configuration changes are picked up quickly
- Hung processes are recovered immediately
- Maximum reliability and uptime

### Q: Can I change the restart interval?

**A**: Yes! Edit `RESTART_INTERVAL=60` in `watchdog-frontends.sh` to any value in seconds.

### Q: What happens during a restart?

**A**: The watchdog:
1. Gracefully terminates all port processes
2. Waits 1 second for ports to release
3. Starts fresh server instances
4. Verifies they're running
5. Logs the results

Total downtime per port: ~3-5 seconds

### Q: Are the ports truly public?

**A**: Yes! All ports use:
- Vite: `host: true` (binds to 0.0.0.0)
- HTTP Server: `-a 0.0.0.0` flag

This makes them accessible from any network interface.

### Q: Can I run individual ports without the watchdog?

**A**: Yes! Use:
```bash
npm run frontend:5555  # Start just port 5555
npm run frontend:6666  # Start just port 6666
# etc.
```

### Q: How do I update a frontend while watchdog is running?

**A**: The watchdog will automatically pick up changes on the next restart cycle (within 60 seconds). For immediate updates:

```bash
# Option 1: Stop, update, restart
npm run watchdog:stop
# Make your changes
npm run watchdog:start

# Option 2: Let it restart automatically
# Just make your changes and wait up to 60 seconds
```

## Related Documentation

- [documentation/guides/FRONTEND_PORTS.md](documentation/guides/FRONTEND_PORTS.md) - Frontend port configuration
- [README.md](README.md) - Main project documentation
- [package.json](package.json) - NPM scripts and dependencies

## Support

For issues or questions:
1. Check the logs: `npm run watchdog:logs`
2. Check the status: `npm run watchdog:status`
3. Review the troubleshooting section above
4. Create an issue in the project repository
