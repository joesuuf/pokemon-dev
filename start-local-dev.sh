#!/bin/bash

# ========================================================================
# Local Development Helper Script
# ========================================================================
# Helps you start the correct development server
# ========================================================================

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}"
echo "========================================================================"
echo "   Pokemon TCG Search - Local Development"
echo "========================================================================"
echo -e "${NC}"
echo ""

echo -e "${CYAN}Which frontend do you want to run?${NC}"
echo ""
echo "  1) React Main Frontend (Port 8888) - PRIMARY"
echo "     • npm run dev"
echo "     • Index: index.html (root)"
echo "     • URL: http://localhost:8888"
echo "     • Full React 19.2.0 + TypeScript + Vite"
echo ""
echo "  2) Static Site (Port 8000) - RECOMMENDED FOR PRODUCTION"
echo "     • python3 -m http.server 8000"
echo "     • Index: static-site/index.html"
echo "     • URL: http://localhost:8000"
echo "     • Pure HTML/CSS/JS (15x smaller, 30x faster)"
echo ""
echo "  3) React Alternative (Port 6666)"
echo "     • npm run dev:6666"
echo "     • Same as main, different port"
echo ""
echo "  4) All Frontends (Multiple ports)"
echo "     • Starts all variants simultaneously"
echo "     • Ports: 5555, 6666, 7777, 8888, 9999"
echo ""
echo "  5) Exit"
echo ""

read -p "Enter your choice (1-5): " CHOICE

case $CHOICE in
    1)
        echo ""
        echo -e "${GREEN}Starting React Main Frontend on port 8888...${NC}"
        echo -e "${CYAN}Index file: index.html (root)${NC}"
        echo -e "${CYAN}URL: http://localhost:8888${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        npm run dev
        ;;
    2)
        echo ""
        echo -e "${GREEN}Starting Static Site on port 8000...${NC}"
        echo -e "${CYAN}Index file: static-site/index.html${NC}"
        echo -e "${CYAN}URL: http://localhost:8000${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""

        # Check if static-site directory exists
        if [ ! -d "static-site" ]; then
            echo -e "${RED}Error: static-site directory not found${NC}"
            exit 1
        fi

        cd static-site

        # Try Python first, then Node.js http-server
        if command -v python3 &> /dev/null; then
            python3 -m http.server 8000
        elif command -v python &> /dev/null; then
            python -m http.server 8000
        elif command -v npx &> /dev/null; then
            npx http-server -p 8000 -c-1
        else
            echo -e "${RED}Error: No HTTP server available${NC}"
            echo "Please install Python 3 or Node.js"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo -e "${GREEN}Starting React Alternative on port 6666...${NC}"
        echo -e "${CYAN}Index file: index.html (root)${NC}"
        echo -e "${CYAN}URL: http://localhost:6666${NC}"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        npm run dev:6666
        ;;
    4)
        echo ""
        echo -e "${GREEN}Starting all frontends...${NC}"
        echo ""
        echo -e "${CYAN}Running on multiple ports:${NC}"
        echo "  • Port 5555: React variant"
        echo "  • Port 6666: Static HTTP server"
        echo "  • Port 7777: Carousel"
        echo "  • Port 8888: Main React"
        echo "  • Port 9999: React variant"
        echo ""
        echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
        echo ""
        npm run frontends:all
        ;;
    5)
        echo ""
        echo -e "${YELLOW}Exiting...${NC}"
        exit 0
        ;;
    *)
        echo ""
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac
