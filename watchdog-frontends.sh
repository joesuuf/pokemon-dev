#!/bin/bash
# Frontend Variants Watchdog Service
# Ensures all frontend ports are persistent, public, and always running
# Restarts each port every minute for maximum reliability

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Configuration
PORTS=(5555 6666 7777 8888 9999)
PIDS=()
LOG_DIR="logs/watchdog"
RESTART_INTERVAL=60  # Restart every 60 seconds

# Create log directory
mkdir -p "$LOG_DIR"

# Get current timestamp
timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Log with timestamp
log() {
    local level=$1
    shift
    local message="$@"
    echo -e "[$(timestamp)] [$level] $message" | tee -a "$LOG_DIR/watchdog.log"
}

# Kill process on port
kill_port() {
    local port=$1
    local killed=false

    if command -v lsof &> /dev/null; then
        local pids=$(lsof -ti :$port 2>/dev/null || true)
        if [ -n "$pids" ]; then
            echo "$pids" | xargs kill -9 2>/dev/null || true
            killed=true
        fi
    elif command -v fuser &> /dev/null; then
        fuser -k ${port}/tcp 2>/dev/null || true
        killed=true
    fi

    if [ "$killed" = true ]; then
        log "INFO" "${YELLOW}Killed process on port $port${NC}"
    fi

    # Wait for port to be fully released
    sleep 1
}

# Check if port is listening
check_port() {
    local port=$1
    if command -v lsof &> /dev/null; then
        lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1
    elif command -v netstat &> /dev/null; then
        netstat -an | grep -q ":$port.*LISTEN"
    else
        return 1
    fi
}

# Start frontend on specific port
start_frontend() {
    local port=$1
    local log_file="$LOG_DIR/port-$port.log"

    log "INFO" "${BLUE}Starting frontend on port $port...${NC}"

    # Kill any existing process on this port
    kill_port $port

    # Start the appropriate server based on port
    case $port in
        6666)
            # Port 6666 uses http-server
            npx http-server frontends/port-6666 -p 6666 -a 0.0.0.0 --cors > "$log_file" 2>&1 &
            ;;
        *)
            # All other ports use vite
            npm run frontend:$port > "$log_file" 2>&1 &
            ;;
    esac

    local pid=$!

    # Wait for server to start
    sleep 3

    # Verify it's running
    if check_port $port; then
        log "INFO" "${GREEN}✅ Port $port started successfully (PID: $pid)${NC}"
        echo $pid
        return 0
    else
        log "ERROR" "${RED}❌ Port $port failed to start${NC}"
        return 1
    fi
}

# Restart all frontends
restart_all() {
    log "INFO" "${MAGENTA}════════════════════════════════════════${NC}"
    log "INFO" "${MAGENTA}  Restarting all frontend variants${NC}"
    log "INFO" "${MAGENTA}════════════════════════════════════════${NC}"

    PIDS=()

    for port in "${PORTS[@]}"; do
        local pid=$(start_frontend $port)
        if [ -n "$pid" ]; then
            PIDS+=($pid)
        fi
    done

    log "INFO" "${GREEN}All frontends restarted!${NC}"
    log "INFO" "${CYAN}Active ports: ${PORTS[*]}${NC}"
    echo ""
}

# Cleanup function
cleanup() {
    log "INFO" "${YELLOW}🛑 Shutting down watchdog...${NC}"

    for port in "${PORTS[@]}"; do
        kill_port $port
    done

    log "INFO" "${GREEN}✅ All frontends stopped${NC}"
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Check dependencies
check_dependencies() {
    if [ ! -d "node_modules" ]; then
        log "INFO" "${YELLOW}⚠️  Installing dependencies...${NC}"
        npm install
        log "INFO" "${GREEN}✅ Dependencies installed!${NC}"
    fi
}

# Main watchdog loop
main() {
    log "INFO" "${GREEN}════════════════════════════════════════${NC}"
    log "INFO" "${GREEN}  Frontend Variants Watchdog Service${NC}"
    log "INFO" "${GREEN}  Restart Interval: ${RESTART_INTERVAL}s${NC}"
    log "INFO" "${GREEN}  Ports: ${PORTS[*]}${NC}"
    log "INFO" "${GREEN}════════════════════════════════════════${NC}"
    echo ""

    # Check dependencies first
    check_dependencies
    echo ""

    # Initial start
    restart_all

    # Watchdog loop - restart every minute
    while true; do
        log "INFO" "${CYAN}Waiting ${RESTART_INTERVAL} seconds until next restart...${NC}"
        sleep $RESTART_INTERVAL
        restart_all
    done
}

# Run main function
main
