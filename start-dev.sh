#!/bin/bash
# Start Both Servers Script
# Starts React front-end and HTML v2 front-end
# Works locally (WSL) and in GitHub Codespaces

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
REACT_PORT=3000
HTML_PORT=8080

# Detect if we're in GitHub Codespaces
is_codespace() {
    [ -n "$CODESPACE_NAME" ] || [ -n "$GITHUB_CODESPACE" ]
}

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

# Check if port is in use
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

# Start React dev server
start_react_server() {
    echo -e "${BLUE}🚀 Starting React dev server on port $REACT_PORT...${NC}"
    
    if check_port $REACT_PORT; then
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
    
    REACT_PID=$!
    
    # Wait a moment for server to start
    sleep 3
    
    echo -e "${GREEN}✅ React server started (PID: $REACT_PID)${NC}"
    
    if is_codespace; then
        CODESPACE_NAME=${CODESPACE_NAME:-$(hostname | tr '[:upper:]' '[:lower:]')}
        echo -e "${CYAN}   Local: http://localhost:$REACT_PORT${NC}"
        echo -e "${CYAN}   Codespace: https://$CODESPACE_NAME-$REACT_PORT.app.github.dev${NC}"
    else
        echo -e "${CYAN}   Access: http://localhost:$REACT_PORT${NC}"
    fi
}

# Start HTML v2 server
start_html_server() {
    echo -e "${BLUE}🚀 Starting HTML v2 server on port $HTML_PORT...${NC}"
    
    if check_port $HTML_PORT; then
        echo -e "${YELLOW}⚠️  Port $HTML_PORT is already in use. Skipping HTML server.${NC}"
        return 0
    fi
    
    # Try Python http.server first (bind to 0.0.0.0 for Codespaces), fallback to http-server
    if command -v python3 &> /dev/null; then
        cd v2
        # Use 0.0.0.0 to allow access from Codespaces
        python3 -m http.server $HTML_PORT --bind 0.0.0.0 > /dev/null 2>&1 &
        HTML_PID=$!
        cd ..
    elif command -v python &> /dev/null; then
        cd v2
        python -m http.server $HTML_PORT --bind 0.0.0.0 > /dev/null 2>&1 &
        HTML_PID=$!
        cd ..
    elif command -v npx &> /dev/null; then
        npx http-server v2 -p $HTML_PORT -a 0.0.0.0 > /dev/null 2>&1 &
        HTML_PID=$!
    else
        echo -e "${RED}❌ No suitable server found. Install Python 3 or Node.js.${NC}"
        exit 1
    fi
    
    # Wait a moment for server to start
    sleep 2
    
    echo -e "${GREEN}✅ HTML v2 server started (PID: $HTML_PID)${NC}"
    
    if is_codespace; then
        CODESPACE_NAME=${CODESPACE_NAME:-$(hostname | tr '[:upper:]' '[:lower:]')}
        echo -e "${CYAN}   Local: http://localhost:$HTML_PORT${NC}"
        echo -e "${CYAN}   Codespace: https://$CODESPACE_NAME-$HTML_PORT.app.github.dev${NC}"
    else
        echo -e "${CYAN}   Access: http://localhost:$HTML_PORT${NC}"
    fi
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    
    if [ ! -z "$REACT_PID" ]; then
        kill $REACT_PID 2>/dev/null || true
        echo -e "${GREEN}✅ React server stopped${NC}"
    fi
    
    if [ ! -z "$HTML_PID" ]; then
        kill $HTML_PID 2>/dev/null || true
        echo -e "${GREEN}✅ HTML server stopped${NC}"
    fi
    
    # Kill any remaining processes on ports
    if command -v lsof &> /dev/null; then
        lsof -ti :$REACT_PORT | xargs kill -9 2>/dev/null || true
        lsof -ti :$HTML_PORT | xargs kill -9 2>/dev/null || true
    fi
    
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Pokémon TCG Dev Servers${NC}"
    if is_codespace; then
        echo -e "${CYAN}  🚀 GitHub Codespaces Mode${NC}"
    else
        echo -e "${CYAN}  💻 WSL/Local Mode${NC}"
    fi
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    
    # Check dependencies
    check_dependencies
    echo ""
    
    # Start servers
    start_react_server
    echo ""
    start_html_server
    
    echo ""
    echo -e "${GREEN}✅ All servers started!${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
    echo ""
    
    # Wait for user interrupt
    wait
}

# Run main function
main

