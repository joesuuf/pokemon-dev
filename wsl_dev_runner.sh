#!/bin/bash
# WSL Dev Server Runner
# Starts all development servers with auto-launch browser

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAIN_PORT=8000
REACT_PORT=3000
BROWSER_DELAY=3

# Detect package manager
detect_package_manager() {
    if command -v pnpm &> /dev/null; then
        echo "pnpm"
    elif command -v yarn &> /dev/null; then
        echo "yarn"
    elif command -v npm &> /dev/null; then
        echo "npm"
    else
        echo "none"
    fi
}

# Check if dependencies are installed
check_dependencies() {
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠️  node_modules not found. Installing dependencies...${NC}"
        
        PM=$(detect_package_manager)
        
        case $PM in
            pnpm)
                pnpm install
                ;;
            yarn)
                yarn install
                ;;
            npm)
                npm install
                ;;
            none)
                echo -e "${RED}❌ No package manager found. Please install npm, yarn, or pnpm.${NC}"
                exit 1
                ;;
        esac
        
        echo -e "${GREEN}✅ Dependencies installed!${NC}"
    fi
}

# Open browser (Windows from WSL)
open_browser() {
    local url=$1
    
    # Try wslview first (if installed)
    if command -v wslview &> /dev/null; then
        wslview "$url" 2>/dev/null && return 0
    fi
    
    # Fallback to cmd.exe
    if command -v cmd.exe &> /dev/null; then
        cmd.exe /c start "$url" 2>/dev/null && return 0
    fi
    
    # Fallback to xdg-open (Linux)
    if command -v xdg-open &> /dev/null; then
        xdg-open "$url" 2>/dev/null && return 0
    fi
    
    echo -e "${YELLOW}⚠️  Could not open browser automatically. Please open manually: $url${NC}"
}

# Start main web server
start_main_server() {
    echo -e "${BLUE}🚀 Starting main web server on port $MAIN_PORT...${NC}"
    
    # Check if port is already in use
    if lsof -Pi :$MAIN_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $MAIN_PORT is already in use. Skipping main server.${NC}"
        return 0
    fi
    
    # Start server in background
    python3 -m http.server $MAIN_PORT > /dev/null 2>&1 &
    MAIN_SERVER_PID=$!
    
    echo -e "${GREEN}✅ Main server started (PID: $MAIN_SERVER_PID)${NC}"
    echo -e "${BLUE}   Access: http://localhost:$MAIN_PORT${NC}"
    
    # Wait a bit then open browser
    sleep 2
    open_browser "http://localhost:$MAIN_PORT/index-test.html"
}

# Start React dev server
start_react_server() {
    echo -e "${BLUE}🚀 Starting React dev server on port $REACT_PORT...${NC}"
    
    # Check if port is already in use
    if lsof -Pi :$REACT_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $REACT_PORT is already in use. Skipping React server.${NC}"
        return 0
    fi
    
    PM=$(detect_package_manager)
    
    case $PM in
        pnpm)
            pnpm run dev &
            ;;
        yarn)
            yarn dev &
            ;;
        npm)
            npm run dev &
            ;;
        none)
            echo -e "${RED}❌ No package manager found.${NC}"
            exit 1
            ;;
    esac
    
    REACT_SERVER_PID=$!
    
    echo -e "${GREEN}✅ React server started (PID: $REACT_SERVER_PID)${NC}"
    echo -e "${BLUE}   Access: http://localhost:$REACT_PORT${NC}"
    
    # Wait a bit then open browser
    sleep $BROWSER_DELAY
    open_browser "http://localhost:$REACT_PORT"
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    
    if [ ! -z "$MAIN_SERVER_PID" ]; then
        kill $MAIN_SERVER_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Main server stopped${NC}"
    fi
    
    if [ ! -z "$REACT_SERVER_PID" ]; then
        kill $REACT_SERVER_PID 2>/dev/null || true
        echo -e "${GREEN}✅ React server stopped${NC}"
    fi
    
    # Kill any remaining processes on ports
    lsof -ti :$MAIN_PORT | xargs kill -9 2>/dev/null || true
    lsof -ti :$REACT_PORT | xargs kill -9 2>/dev/null || true
    
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  WSL Dev Server Runner${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    
    # Check dependencies
    check_dependencies
    
    echo ""
    
    # Start servers
    start_main_server
    echo ""
    start_react_server
    
    echo ""
    echo -e "${GREEN}✅ All servers started!${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
    echo ""
    
    # Wait for user interrupt
    wait
}

# Run main function
main
