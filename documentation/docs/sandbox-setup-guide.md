# Sandbox Container Setup Guide

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Detailed Setup Process](#detailed-setup-process)
5. [Working with the Dev Branch](#working-with-the-dev-branch)
6. [Managing Dependencies](#managing-dependencies)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Overview

This guide provides a comprehensive, step-by-step process for setting up a safe sandbox container environment where you can experiment with code changes without affecting your main development environment.

### What You'll Learn
- How to create an isolated Docker container for development
- How to import and work with your dev branch
- How to manage project dependencies safely
- How to iterate on changes without risk

### Why Use a Sandbox?
- **Isolation**: Changes don't affect your host system
- **Safety**: Experiment freely without breaking your main environment
- **Reproducibility**: Easy to reset and start fresh
- **Consistency**: Same environment across different machines

---

## Prerequisites

### Required Software

#### 1. Docker
Docker provides the containerization needed for the sandbox.

**Check if Docker is installed:**
```bash
docker --version
```

**Installation:**
- **macOS**: Download [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- **Windows**: Download [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- **Linux (Ubuntu/Debian)**:
  ```bash
  # Update package index
  sudo apt-get update

  # Install prerequisites
  sudo apt-get install ca-certificates curl gnupg

  # Add Docker's official GPG key
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  # Set up repository
  echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  # Install Docker Engine
  sudo apt-get update
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  ```

**Verify installation:**
```bash
# Test Docker
docker run hello-world

# Check Docker Compose
docker compose version
```

#### 2. Git
Git is required to clone and manage your repository.

**Check if Git is installed:**
```bash
git --version
```

**Installation:**
- **macOS**: `brew install git` or download from [git-scm.com](https://git-scm.com/)
- **Windows**: Download from [git-scm.com](https://git-scm.com/)
- **Linux**: `sudo apt-get install git`

#### 3. Text Editor (Optional but Recommended)
- VS Code with Docker extension
- Vim/Nano for terminal editing

---

## Quick Start

### 5-Minute Setup

```bash
# 1. Create project directory
mkdir -p ~/sandbox-projects/pokemon-dev-sandbox
cd ~/sandbox-projects/pokemon-dev-sandbox

# 2. Clone your repository
git clone https://github.com/joesuuf/pokemon-dev.git .
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# 3. Create Dockerfile
cat > Dockerfile << 'EOF'
FROM node:18-alpine

WORKDIR /app

# Install git and basic tools
RUN apk add --no-cache git bash

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Expose dev server port
EXPOSE 3000

# Default command
CMD ["npm", "run", "dev"]
EOF

# 4. Build and run
docker build -t pokemon-dev-sandbox .
docker run -it -p 3000:3000 -v $(pwd):/app pokemon-dev-sandbox
```

**That's it!** Your sandbox is running at `http://localhost:3000`

---

## Detailed Setup Process

### Step 1: Prepare Your Workspace

Create a dedicated directory for sandbox projects to keep things organized.

```bash
# Create sandbox workspace
# This keeps sandbox projects separate from your main development
mkdir -p ~/sandbox-projects

# Navigate to the workspace
cd ~/sandbox-projects

# Create project-specific sandbox directory
mkdir pokemon-dev-sandbox
cd pokemon-dev-sandbox
```

**Why?** Separating sandbox projects prevents confusion and makes cleanup easier.

---

### Step 2: Clone the Repository

#### Option A: Clone from Remote (Recommended)

```bash
# Clone the repository
# This creates a fresh copy isolated from your main development
git clone https://github.com/joesuuf/pokemon-dev.git .

# Verify the clone
ls -la
# You should see: package.json, src/, public/, etc.
```

#### Option B: Clone from Local Repository

```bash
# If you want to use your local repo as the source
git clone /path/to/your/local/pokemon-dev .

# Example:
# git clone ~/projects/pokemon-dev .
```

**Understanding the clone:**
- The `.` at the end clones into the current directory
- You get a complete copy with full git history
- Changes here won't affect your original repository

---

### Step 3: Checkout the Dev Branch

```bash
# List all available branches
git branch -a

# Checkout the specific dev branch
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Verify you're on the correct branch
git branch
# Should show: * claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Check the current status
git status
# Should show: "nothing to commit, working tree clean"
```

**Branch naming convention:**
- `claude/` prefix indicates Claude-generated branches
- The long suffix is a unique session identifier
- This ensures no conflicts with other branches

---

### Step 4: Create the Dockerfile

The Dockerfile defines your sandbox environment.

```bash
# Create the Dockerfile
cat > Dockerfile << 'EOF'
# Use Node.js 18 Alpine (lightweight Linux distribution)
# Alpine is chosen for its small size (~5MB base) and security
FROM node:18-alpine

# Set the working directory inside the container
# All subsequent commands will run from this directory
WORKDIR /app

# Install essential tools
# git: Required for any git operations inside the container
# bash: Provides a better shell than Alpine's default sh
# python3, make, g++: Required for some npm packages with native dependencies
RUN apk add --no-cache \
    git \
    bash \
    python3 \
    make \
    g++

# Copy package files first (Docker layer caching optimization)
# By copying these separately, we can cache the npm install step
# This means faster rebuilds when only source code changes
COPY package*.json ./

# Install Node.js dependencies
# --frozen-lockfile ensures the lockfile isn't modified
# This guarantees consistent dependency versions
RUN npm install --frozen-lockfile

# Copy the rest of the application
# Done after npm install to leverage Docker's layer caching
COPY . .

# Expose the development server port
# This makes the port available to your host machine
EXPOSE 3000

# Set environment to development
ENV NODE_ENV=development

# Default command when container starts
# Can be overridden with docker run command
CMD ["npm", "run", "dev"]
EOF

# Verify the Dockerfile was created
cat Dockerfile
```

**Understanding the Dockerfile:**
- **FROM**: Base image (Node.js 18 on Alpine Linux)
- **WORKDIR**: Sets the working directory to `/app`
- **RUN**: Executes commands during build
- **COPY**: Copies files from host to container
- **EXPOSE**: Documents which ports are used
- **CMD**: Default command when container starts

---

### Step 5: Create Docker Compose Configuration (Optional but Recommended)

Docker Compose makes managing containers easier.

```bash
# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  # Main development service
  dev:
    # Build from the local Dockerfile
    build:
      context: .
      dockerfile: Dockerfile

    # Container name (easier to reference)
    container_name: pokemon-dev-sandbox

    # Port mapping: host:container
    # Access the app at localhost:3000
    ports:
      - "3000:3000"

    # Volume mounts for live code editing
    # Changes on your host immediately reflect in the container
    volumes:
      - .:/app                          # Mount project directory
      - /app/node_modules               # Preserve container's node_modules

    # Environment variables
    environment:
      - NODE_ENV=development
      - VITE_API_KEY=${VITE_API_KEY}   # Pass through API keys

    # Restart policy
    restart: unless-stopped

    # Keep container running
    stdin_open: true
    tty: true

    # Override default command for development
    command: npm run dev

  # Optional: Test runner service
  test:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: pokemon-dev-test
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=test
    command: npm run test:watch
    profiles:
      - testing  # Only starts with --profile testing

  # Optional: Build verification service
  build:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: pokemon-dev-build
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run build
    profiles:
      - build  # Only starts with --profile build
EOF

# Verify docker-compose.yml
cat docker-compose.yml
```

**Benefits of Docker Compose:**
- Define multiple services (dev, test, build)
- Easy environment variable management
- Simple start/stop commands
- Volume management handled automatically

---

### Step 6: Create Environment Configuration

```bash
# Create .env file for local development
cat > .env << 'EOF'
# Development Environment Variables
NODE_ENV=development

# Vite Configuration
VITE_PORT=3000

# API Keys (replace with your actual keys)
VITE_API_KEY=your-pokemon-tcg-api-key-here

# Optional: Enable debug mode
DEBUG=true
VITE_DEBUG=true
EOF

# Create .env.example for documentation
cp .env .env.example

# Secure the .env file (contains secrets)
chmod 600 .env

echo "Created .env file - REMEMBER TO ADD YOUR ACTUAL API KEYS"
```

**Security Note:**
- Never commit `.env` with real API keys
- Use `.env.example` to document required variables
- The `.gitignore` should already exclude `.env`

---

### Step 7: Create .dockerignore

Prevent unnecessary files from being copied into the Docker image.

```bash
# Create .dockerignore
cat > .dockerignore << 'EOF'
# Dependencies
node_modules
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Testing
coverage
.nyc_output

# Build output
dist
build

# Environment files
.env
.env.local
.env.*.local

# IDE
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Git
.git
.gitignore
.gitattributes

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Documentation
*.md
docs/

# CI/CD
.github
.gitlab-ci.yml
EOF
```

**Why .dockerignore?**
- Reduces image size
- Speeds up build times
- Prevents copying sensitive files
- Keeps images clean

---

### Step 8: Build the Docker Image

```bash
# Build the Docker image
# -t tags the image with a name
# . specifies the build context (current directory)
docker build -t pokemon-dev-sandbox .

# You'll see output like:
# [+] Building 45.2s (12/12) FINISHED
# => [internal] load build definition
# => [internal] load .dockerignore
# => [internal] load metadata
# => [1/6] FROM docker.io/library/node:18-alpine
# => [2/6] WORKDIR /app
# => [3/6] RUN apk add --no-cache git bash
# => [4/6] COPY package*.json ./
# => [5/6] RUN npm install
# => [6/6] COPY . .
# => exporting to image
# => => naming to docker.io/library/pokemon-dev-sandbox

# Verify the image was created
docker images | grep pokemon-dev-sandbox

# Expected output:
# pokemon-dev-sandbox   latest   abc123def456   2 minutes ago   450MB
```

**Understanding the build:**
- Each line in Dockerfile creates a layer
- Layers are cached for faster rebuilds
- Build time depends on internet speed (for npm install)

---

### Step 9: Run the Sandbox Container

#### Method A: Using Docker Run (Simple)

```bash
# Run the container interactively
docker run -it \
  --name pokemon-sandbox-instance \
  -p 3000:3000 \
  -v $(pwd):/app \
  -v /app/node_modules \
  --env-file .env \
  pokemon-dev-sandbox

# Explanation of flags:
# -it              : Interactive terminal
# --name           : Give the container a name
# -p 3000:3000     : Map port 3000 (host:container)
# -v $(pwd):/app   : Mount current directory to /app
# -v /app/node_modules : Prevent overwriting node_modules
# --env-file .env  : Load environment variables
# pokemon-dev-sandbox : The image name to use
```

#### Method B: Using Docker Compose (Recommended)

```bash
# Start all services defined in docker-compose.yml
docker compose up

# Or run in detached mode (background)
docker compose up -d

# View logs
docker compose logs -f

# Start with specific profile (e.g., testing)
docker compose --profile testing up

# Stop services
docker compose down

# Stop and remove volumes
docker compose down -v
```

**Verification:**
1. Open your browser to `http://localhost:3000`
2. You should see your Pokemon TCG application
3. Check container logs for any errors

---

### Step 10: Working Inside the Container

#### Enter the Running Container

```bash
# Method 1: Using docker exec (container must be running)
docker exec -it pokemon-sandbox-instance bash

# Method 2: Using docker compose
docker compose exec dev bash

# You're now inside the container at /app
# Your prompt should change to something like: root@abc123:/app#
```

#### Common Commands Inside the Container

```bash
# Check Node.js version
node --version

# Check npm version
npm --version

# List installed packages
npm list --depth=0

# Run tests
npm run test

# Run build
npm run build

# Check git status
git status

# View project structure
ls -la

# Exit the container
exit
```

---

## Working with the Dev Branch

### Keeping Your Sandbox Up to Date

#### Fetch Latest Changes

```bash
# From your host machine (not inside container)
cd ~/sandbox-projects/pokemon-dev-sandbox

# Fetch changes from remote
git fetch origin

# View changes
git log HEAD..origin/claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Pull changes
git pull origin claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# If using Docker Compose, restart to apply changes
docker compose restart
```

#### Creating Experimental Branches

```bash
# Create a new branch for experiments
git checkout -b sandbox/my-experiment

# Make changes...
# Test them...

# If experiment succeeds, merge it back
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg
git merge sandbox/my-experiment

# If experiment fails, just delete the branch
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg
git branch -D sandbox/my-experiment
```

---

## Managing Dependencies

### Creating requirements.txt for Node.js Projects

While `requirements.txt` is Python-specific, here's how to manage dependencies:

#### package.json (Node.js equivalent)

Your `package.json` already lists dependencies:

```json
{
  "dependencies": {
    "@types/axios": "^0.9.36",
    "axios": "^1.12.2",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.1.16",
    "tailwindcss": "^4.1.16",
    "vite": "^7.1.12",
    "vitest": "^4.0.3"
  }
}
```

#### Installing Dependencies in Container

```bash
# Inside container or via docker exec

# Install all dependencies
npm install

# Install specific package
npm install package-name

# Install specific version
npm install package-name@1.2.3

# Install dev dependency
npm install --save-dev package-name

# Update dependencies
npm update

# Audit for vulnerabilities
npm audit

# Fix vulnerabilities automatically
npm audit fix
```

#### Freezing Dependencies

```bash
# Inside container

# Generate package-lock.json (if not exists)
npm install

# This locks exact versions of all dependencies
# Commit package-lock.json to ensure consistency

# To install from locked versions
npm ci  # Faster and more reliable than npm install
```

### Custom requirements.txt Template

Create a custom file for additional system requirements:

```bash
# Create a custom requirements file
cat > system-requirements.txt << 'EOF'
# System Requirements for Pokemon TCG Dev Sandbox

## Node.js Packages (installed via npm)
# See package.json for the complete list

## System Tools (installed via apk in Dockerfile)
git
bash
python3
make
g++

## Optional: Python packages if needed
# Uncomment if you need Python tools
# pip3 install --no-cache-dir \
#     pylint \
#     black \
#     pytest

## Optional: Additional tools
# curl
# wget
# vim
# nano
EOF
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Port Already in Use

**Error:** `Error starting userland proxy: listen tcp4 0.0.0.0:3000: bind: address already in use`

**Solution:**
```bash
# Find what's using port 3000
lsof -i :3000
# or
sudo netstat -tulpn | grep :3000

# Kill the process (replace PID with actual process ID)
kill -9 PID

# Or use a different port
docker run -p 3001:3000 pokemon-dev-sandbox
```

#### Issue 2: Docker Build Fails

**Error:** Various build errors

**Solution:**
```bash
# Clean up Docker cache
docker builder prune

# Rebuild without cache
docker build --no-cache -t pokemon-dev-sandbox .

# Check Docker disk space
docker system df

# Clean up if needed
docker system prune -a
```

#### Issue 3: Container Keeps Restarting

**Solution:**
```bash
# Check container logs
docker logs pokemon-sandbox-instance

# Check last 100 lines
docker logs --tail 100 pokemon-sandbox-instance

# Follow logs in real-time
docker logs -f pokemon-sandbox-instance

# Inspect container
docker inspect pokemon-sandbox-instance
```

#### Issue 4: Changes Not Reflecting

**Problem:** You edit files but don't see changes in the container

**Solution:**
```bash
# Ensure volume is mounted correctly
docker inspect pokemon-sandbox-instance | grep Mounts -A 20

# Restart the container
docker restart pokemon-sandbox-instance

# Or recreate the container
docker compose down
docker compose up -d
```

#### Issue 5: npm install Fails

**Error:** Network errors or permission issues

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try with different registry
npm install --registry=https://registry.npmjs.org/

# Inside container, try with sudo if permission error
# (though you're usually root in Alpine containers)

# Rebuild with verbose logging
docker build --progress=plain -t pokemon-dev-sandbox .
```

#### Issue 6: Container Out of Memory

**Solution:**
```bash
# Increase Docker memory limit in Docker Desktop settings
# Settings > Resources > Memory

# Or run with memory limit
docker run --memory="4g" pokemon-dev-sandbox

# In docker-compose.yml, add:
# deploy:
#   resources:
#     limits:
#       memory: 4G
```

---

## Advanced Configuration

### Multi-Stage Builds for Optimization

Create a more efficient Dockerfile:

```dockerfile
# Stage 1: Build dependencies
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Stage 2: Development build
FROM node:18-alpine AS development
WORKDIR /app
RUN apk add --no-cache git bash
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Stage 3: Production build
FROM node:18-alpine AS production
WORKDIR /app
RUN apk add --no-cache git bash
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Health Checks

Add health check to docker-compose.yml:

```yaml
services:
  dev:
    # ... other config ...
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Networking with Other Containers

```yaml
# docker-compose.yml with multiple services
version: '3.8'

networks:
  pokemon-network:
    driver: bridge

services:
  dev:
    # ... existing config ...
    networks:
      - pokemon-network

  # Example: Add a database
  postgres:
    image: postgres:15-alpine
    container_name: pokemon-db
    environment:
      POSTGRES_USER: pokemon
      POSTGRES_PASSWORD: pokemon
      POSTGRES_DB: pokemon_tcg
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - pokemon-network

volumes:
  postgres-data:
```

### Cleanup Scripts

Create a cleanup script:

```bash
cat > cleanup-sandbox.sh << 'EOF'
#!/bin/bash
# Cleanup script for Pokemon Dev Sandbox

echo "Stopping containers..."
docker compose down

echo "Removing images..."
docker rmi pokemon-dev-sandbox

echo "Pruning unused resources..."
docker system prune -f

echo "Cleanup complete!"
EOF

chmod +x cleanup-sandbox.sh
```

---

## Best Practices

### 1. Version Control

```bash
# Always commit working changes before experimenting
git add .
git commit -m "Working state before sandbox experiments"

# Create experiment branches
git checkout -b sandbox/experiment-name
```

### 2. Resource Management

```bash
# Regularly clean up Docker resources
docker system prune -a --volumes

# Monitor Docker disk usage
docker system df
```

### 3. Security

```bash
# Never commit .env files
echo ".env" >> .gitignore

# Use .env.example for documentation
cp .env .env.example
# Remove actual values from .env.example
```

### 4. Documentation

```bash
# Document your experiments
mkdir -p docs/sandbox-experiments
echo "# Experiment: $(date)" > docs/sandbox-experiments/$(date +%Y%m%d).md
```

### 5. Backup

```bash
# Regularly backup your sandbox state
docker commit pokemon-sandbox-instance pokemon-dev-backup:$(date +%Y%m%d)

# Export if needed
docker save pokemon-dev-backup:$(date +%Y%m%d) | gzip > backup-$(date +%Y%m%d).tar.gz
```

---

## Quick Reference Commands

```bash
# Build
docker build -t pokemon-dev-sandbox .

# Run (simple)
docker run -it -p 3000:3000 pokemon-dev-sandbox

# Run (with compose)
docker compose up -d

# Stop
docker compose down

# Logs
docker compose logs -f

# Execute command in container
docker exec -it pokemon-sandbox-instance npm test

# Shell access
docker exec -it pokemon-sandbox-instance bash

# Rebuild
docker compose build --no-cache

# Remove everything
docker compose down -v
docker rmi pokemon-dev-sandbox
```

---

## Next Steps

1. **Test the Setup**: Access http://localhost:3000 and verify the app works
2. **Review Tailwind Guide**: See `tailwind-v4-guide.md` for Tailwind CSS setup
3. **Review Claude Code Guide**: See `anthropic-claude-code-guide.md` for AI assistance
4. **Start Experimenting**: Create a branch and try new features safely!

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Node.js Docker Best Practices](https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md)
- [Vite Docker Configuration](https://vitejs.dev/guide/env-and-mode.html)

---

**Happy Sandboxing! 🚀**
