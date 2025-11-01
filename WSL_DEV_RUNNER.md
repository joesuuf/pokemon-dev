# WSL Dev Runner Script

## Problem Fixed

You were trying to run a shell script with Python:
```bash
# ❌ WRONG - Don't do this
python3 wsl_dev_runner.sh
```

Shell scripts (`.sh` files) must be run with `bash`, not Python.

## Solution: Run with Bash

```bash
# ✅ CORRECT - Run with bash
bash wsl_dev_runner.sh
```

## Make Executable (Optional)

In WSL, you can make it executable:

```bash
chmod +x wsl_dev_runner.sh
./wsl_dev_runner.sh
```

## What the Script Does

The `wsl_dev_runner.sh` script:

1. **Auto-detects package manager** (npm/yarn/pnpm)
2. **Checks dependencies** - Installs `node_modules` if missing
3. **Starts main web server** - Port 8000 (Python HTTP server)
4. **Starts React dev server** - Port 3000 (Vite)
5. **Auto-launches browser** - Opens testing hub automatically
6. **Clean shutdown** - Press Ctrl+C to stop all servers

## Usage

### Basic Usage (WSL terminal):

```bash
bash wsl_dev_runner.sh
```

### Or make executable first:

```bash
chmod +x wsl_dev_runner.sh
./wsl_dev_runner.sh
```

## Features

- ✅ Auto-installs dependencies if `node_modules` missing
- ✅ Auto-detects npm/yarn/pnpm
- ✅ Checks if ports are already in use
- ✅ Auto-launches browser (wslview → cmd.exe → xdg-open)
- ✅ Color-coded output
- ✅ Proper cleanup on Ctrl+C
- ✅ Runs both servers simultaneously

## Output

When you run it, you'll see:

```
════════════════════════════════════════
  WSL Dev Server Runner
════════════════════════════════════════

🚀 Starting main web server on port 8000...
✅ Main server started (PID: 12345)
   Access: http://localhost:8000

🚀 Starting React dev server on port 3000...
✅ React server started (PID: 12346)
   Access: http://localhost:3000

✅ All servers started!
Press Ctrl+C to stop all servers
```

## Troubleshooting

### Issue: "Permission denied"
**Solution:**
```bash
chmod +x wsl_dev_runner.sh
```

### Issue: "bash: command not found"
**Solution:** Make sure you're in WSL, not Windows PowerShell

### Issue: "No package manager found"
**Solution:** Install npm:
```bash
sudo apt update
sudo apt install nodejs npm
```

### Issue: Port already in use
**Solution:** Kill processes on ports:
```bash
lsof -ti :8000 | xargs kill -9
lsof -ti :3000 | xargs kill -9
```

## Quick Commands

```bash
# Run the script
bash wsl_dev_runner.sh

# Or with executable
chmod +x wsl_dev_runner.sh && ./wsl_dev_runner.sh

# Stop all servers (Ctrl+C)
```

## Manual Alternative

If the script doesn't work, run manually:

```bash
# Terminal 1: Main server
python3 -m http.server 8000 &
sleep 2 && cmd.exe /c start http://localhost:8000/index-test.html

# Terminal 2: React server
npm install  # First time only
npm run dev && sleep 3 && cmd.exe /c start http://localhost:3000
```

