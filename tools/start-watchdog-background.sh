#!/bin/bash
# Start Watchdog in Background
# Runs the frontend watchdog service in the background with nohup

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WATCHDOG_SCRIPT="$SCRIPT_DIR/watchdog-frontends.sh"
PID_FILE="$SCRIPT_DIR/logs/watchdog/watchdog.pid"
LOG_FILE="$SCRIPT_DIR/logs/watchdog/watchdog-background.log"

# Create log directory
mkdir -p "$SCRIPT_DIR/logs/watchdog"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "Watchdog is already running (PID: $PID)"
        echo "To stop it, run: kill $PID"
        exit 1
    else
        echo "Removing stale PID file..."
        rm -f "$PID_FILE"
    fi
fi

# Start watchdog in background
echo "Starting Frontend Watchdog in background..."
nohup "$WATCHDOG_SCRIPT" > "$LOG_FILE" 2>&1 &
WATCHDOG_PID=$!

# Save PID
echo $WATCHDOG_PID > "$PID_FILE"

echo "✅ Watchdog started successfully!"
echo "   PID: $WATCHDOG_PID"
echo "   Log: $LOG_FILE"
echo "   PID File: $PID_FILE"
echo ""
echo "To stop the watchdog, run:"
echo "   kill $WATCHDOG_PID"
echo "   or"
echo "   npm run watchdog:stop"
echo ""
echo "To view logs:"
echo "   tail -f $LOG_FILE"
