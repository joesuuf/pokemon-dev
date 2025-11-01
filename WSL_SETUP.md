# WSL Setup and Troubleshooting Guide

## Issue: "next: not found" Error

If you're getting an error like:
```
> pokemon-card-gallery@1.0.0 dev
> next dev
sh: 1: next: not found
```

**This means:**
- Dependencies are not installed (`node_modules` missing)
- The project uses **Vite**, not Next.js

## Solution: Install Dependencies

Run this command in your **WSL terminal**:

```bash
npm install
```

This will install all dependencies including Vite and React.

## Verify Installation

After installation, verify the dev script:

```bash
npm run dev
```

This should start Vite dev server, not Next.js.

## Quick Start Commands (WSL)

### 1. Install dependencies (first time only):
```bash
npm install
```

### 2. Start React dev server:
```bash
npm run dev
```

### 3. Start React dev server with auto-launch:
```bash
npm run dev && sleep 3 && cmd.exe /c start http://localhost:3000
```

### 4. Or use wslview (if installed):
```bash
npm run dev && sleep 3 && wslview http://localhost:3000
```

## Common Issues

### Issue 1: npm not found
**Solution:** Install Node.js in WSL:
```bash
# Ubuntu/Debian
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Or use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
```

### Issue 2: Wrong package manager
Make sure you're using npm, not yarn or pnpm.

### Issue 3: Port already in use
If port 3000 is already in use:
```bash
# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
# Or find and kill manually
netstat -tulpn | grep :3000
```

### Issue 4: Permissions error
```bash
# Fix npm permissions
sudo chown -R $(whoami) ~/.npm
sudo chown -R $(whoami) node_modules
```

## Verify Your Setup

1. **Check Node.js version:**
   ```bash
   node --version
   # Should be 18.x or higher
   ```

2. **Check npm version:**
   ```bash
   npm --version
   # Should be 9.x or higher
   ```

3. **Check if node_modules exists:**
   ```bash
   ls -la node_modules
   ```

4. **Verify package.json dev script:**
   ```bash
   cat package.json | grep '"dev"'
   # Should show: "dev": "vite"
   ```

## Correct dev Script

The `package.json` should have:
```json
"scripts": {
  "dev": "vite"
}
```

NOT:
```json
"dev": "next dev"
```

If you see `"next dev"`, something is wrong with your package.json.

## Full Setup Commands (WSL)

```bash
# 1. Navigate to project directory
cd /mnt/c/claude-code/_projects/pokemon/pokemon-dev-v0.4

# 2. Install dependencies
npm install

# 3. Start dev server with auto-launch
npm run dev && sleep 3 && cmd.exe /c start http://localhost:3000
```

## Alternative: Use Vite Preview

If dev server has issues, try preview mode after building:

```bash
npm run build
npm run preview
```

## Need Help?

Check these files:
- `package.json` - Verify scripts and dependencies
- `vite.config.ts` - Verify Vite configuration
- Check browser console for errors
- Check terminal for detailed error messages

