#!/bin/bash
# Stop Watchdog Service
# Gracefully stops the frontend watchdog service

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/logs/watchdog/watchdog.pid"

# Check if PID file exists
if [ ! -f "$PID_FILE" ]; then
    echo "❌ Watchdog is not running (no PID file found)"
    exit 1
fi

# Read PID
PID=$(cat "$PID_FILE")

# Check if process is running
if ! ps -p $PID > /dev/null 2>&1; then
    echo "❌ Watchdog process not found (PID: $PID)"
    echo "Removing stale PID file..."
    rm -f "$PID_FILE"
    exit 1
fi

# Kill the watchdog process and all child processes
echo "Stopping Frontend Watchdog (PID: $PID)..."
pkill -P $PID 2>/dev/null || true
kill $PID 2>/dev/null || true

# Wait a moment
sleep 2

# Force kill if still running
if ps -p $PID > /dev/null 2>&1; then
    echo "Force killing watchdog..."
    kill -9 $PID 2>/dev/null || true
fi

# Kill all processes on frontend ports
echo "Cleaning up frontend ports..."
for port in 5555 6666 7777 8888 9999; do
    if command -v lsof &> /dev/null; then
        lsof -ti :$port 2>/dev/null | xargs kill -9 2>/dev/null || true
    elif command -v fuser &> /dev/null; then
        fuser -k ${port}/tcp 2>/dev/null || true
    fi
done

# Remove PID file
rm -f "$PID_FILE"

echo "✅ Watchdog stopped successfully!"
echo "   All frontend ports have been cleaned up."
