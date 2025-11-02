#!/bin/bash
# Check Watchdog Status
# Shows the current status of the watchdog and all frontend ports

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/logs/watchdog/watchdog.pid"
PORTS=(5555 6666 7777 8888 9999)

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}════════════════════════════════════════${NC}"
echo -e "${CYAN}  Frontend Watchdog Status${NC}"
echo -e "${CYAN}════════════════════════════════════════${NC}"
echo ""

# Check watchdog process
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Watchdog: RUNNING (PID: $PID)${NC}"
    else
        echo -e "${RED}❌ Watchdog: NOT RUNNING (stale PID file)${NC}"
    fi
else
    echo -e "${RED}❌ Watchdog: NOT RUNNING${NC}"
fi

echo ""
echo -e "${CYAN}Frontend Port Status:${NC}"
echo ""

# Check each port
for port in "${PORTS[@]}"; do
    if command -v lsof &> /dev/null; then
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            PID=$(lsof -ti :$port)
            echo -e "  Port $port: ${GREEN}✅ RUNNING${NC} (PID: $PID)"
        else
            echo -e "  Port $port: ${RED}❌ NOT RUNNING${NC}"
        fi
    elif command -v netstat &> /dev/null; then
        if netstat -an | grep -q ":$port.*LISTEN"; then
            echo -e "  Port $port: ${GREEN}✅ RUNNING${NC}"
        else
            echo -e "  Port $port: ${RED}❌ NOT RUNNING${NC}"
        fi
    else
        echo -e "  Port $port: ${YELLOW}⚠️  CANNOT CHECK (no lsof/netstat)${NC}"
    fi
done

echo ""
echo -e "${CYAN}Access URLs:${NC}"
for port in "${PORTS[@]}"; do
    echo "  http://localhost:$port"
done

echo ""
