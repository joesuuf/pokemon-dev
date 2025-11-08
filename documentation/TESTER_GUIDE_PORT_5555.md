# Site Tester Guide: Starting Port 5555 React Frontend

**Version:** 1.0  
**Last Updated:** November 2025  
**For:** Site Testers & QA Team

---

## 📋 Overview

This guide will walk you through starting the main React frontend application on port 5555. This is a **step-by-step, hand-holding guide** designed for testers who may not be familiar with command-line tools.

**What you'll be starting:** A Pokemon Trading Card Game search application built with React and TypeScript.

**Estimated time:** 5-10 minutes (first time), 2-3 minutes (subsequent starts)

---

## ✅ Prerequisites Checklist

Before you begin, make sure you have:

- [ ] **Access to the machine** (local or remote via SSH/Codespaces)
- [ ] **Node.js installed** (version 18 or higher)
- [ ] **npm installed** (comes with Node.js)
- [ ] **Project code downloaded/cloned** to your machine
- [ ] **Terminal/Command Prompt** access

### How to Check Prerequisites

**Check Node.js version:**
```bash
node --version
```
✅ **Good:** `v18.x.x` or higher (e.g., `v20.10.0`)  
❌ **Problem:** Command not found or version below 18

**Check npm version:**
```bash
npm --version
```
✅ **Good:** `9.x.x` or higher  
❌ **Problem:** Command not found

**If Node.js/npm are missing:**
- Download from: https://nodejs.org/
- Install the LTS (Long Term Support) version
- Restart your terminal after installation

---

## 🚀 Step-by-Step Startup Instructions

### Step 1: Open Your Terminal

**On Windows:**
- Press `Win + R`, type `cmd`, press Enter
- OR search for "Command Prompt" in Start menu
- OR right-click in the project folder and select "Open in Terminal"

**On Mac/Linux:**
- Press `Cmd + Space` (Mac) or `Ctrl + Alt + T` (Linux)
- Type "Terminal" and press Enter
- OR right-click in the project folder and select "Open in Terminal"

**In VS Code/Cursor:**
- Press `` Ctrl + ` `` (backtick) to open integrated terminal
- OR go to: Terminal → New Terminal

---

### Step 2: Navigate to Project Directory

You need to be in the project's root directory (where `package.json` is located).

**Check if you're in the right place:**
```bash
ls package.json
```
✅ **Good:** Shows `package.json`  
❌ **Problem:** `No such file or directory`

**If you're not in the right directory:**

**On Windows:**
```bash
cd C:\path\to\pokemon-dev
```
*(Replace with your actual project path)*

**On Mac/Linux:**
```bash
cd /path/to/pokemon-dev
```
*(Replace with your actual project path)*

**In Codespaces/GitHub:**
The terminal usually opens in the workspace directory automatically. If not:
```bash
cd /workspace
```

---

### Step 3: Install Dependencies (First Time Only)

**⚠️ IMPORTANT:** Only needed the first time you set up the project, or after pulling new changes.

**Check if node_modules exists:**
```bash
ls node_modules
```
✅ **Good:** Shows a list of folders  
❌ **Problem:** `No such file or directory` → You need to install dependencies

**Install dependencies:**
```bash
npm install
```

**What to expect:**
- This may take 2-5 minutes
- You'll see lots of text scrolling by
- Look for: `added XXX packages` at the end
- ✅ **Success:** Ends with "audited XXX packages" and no errors

**Common issues:**
- ❌ **"npm: command not found"** → Node.js not installed or not in PATH
- ❌ **"EACCES" or permission errors** → Try: `sudo npm install` (Mac/Linux) or run as Administrator (Windows)
- ❌ **Network timeout** → Check internet connection, try again

---

### Step 4: Start the Server

**Run the startup command:**
```bash
npm run frontend:5555
```

**What to expect:**
- You'll see Vite starting up
- Look for messages like:
  ```
  VITE v7.x.x  ready in XXX ms
  
  ➜  Local:   http://localhost:5555/
  ➜  Network: http://0.0.0.0:5555/
  ➜  press h to show help
  ```
- ✅ **Success:** Server is running when you see "ready" and the URL

**Keep the terminal open!** The server runs in this window. Closing it will stop the server.

---

### Step 5: Access the Application

**Open your web browser** (Chrome, Firefox, Safari, Edge, etc.)

**For local access:**
- Go to: `http://localhost:5555`
- OR: `http://127.0.0.1:5555`

**For remote access (Codespaces/WSL/Remote Server):**
- Check the terminal output for the Network URL
- It will look like: `http://0.0.0.0:5555`
- Use your machine's IP address or Codespaces URL instead
- Example: `http://your-ip-address:5555`
- Example (Codespaces): `https://your-codespace-name-5555.app.github.dev`

**What you should see:**
- ✅ Pokemon TCG Search application homepage
- ✅ Search bar at the top
- ✅ View mode toggle buttons
- ✅ Empty state or welcome message

**If you see an error:**
- ❌ **"This site can't be reached"** → Server might not be running, check Step 4
- ❌ **"Connection refused"** → Port 5555 might be blocked by firewall
- ❌ **Blank page** → Check browser console (F12) for errors

---

## 🎯 Verification Checklist

Use this checklist to confirm everything is working:

- [ ] Terminal shows "VITE ready" message
- [ ] Browser successfully loads `http://localhost:5555`
- [ ] Page displays Pokemon TCG Search interface
- [ ] Search bar is visible and functional
- [ ] No error messages in browser console (F12 → Console tab)
- [ ] No error messages in terminal

---

## 🧪 Quick Functionality Test

Once the application is loaded, test these basic features:

1. **Search Test:**
   - Type "Pikachu" in the search bar
   - Press Enter or click Search
   - ✅ Should show Pokemon cards with Pikachu

2. **View Mode Test:**
   - Click "Card Grid View" button
   - Click "Detailed List View" button
   - ✅ Should switch between different display modes

3. **Card Details Test:**
   - Click on any card in the results
   - ✅ Should show detailed card information

---

## 🛑 Stopping the Server

**To stop the server:**
1. Go back to your terminal window
2. Press `Ctrl + C` (Windows/Linux) or `Cmd + C` (Mac)
3. Wait for the process to stop
4. ✅ You should see the command prompt return

**Note:** Closing the terminal window will also stop the server, but using `Ctrl+C` is the proper way.

---

## 🔧 Troubleshooting Guide

### Problem: "Port 5555 is already in use"

**Symptoms:**
- Error message: `Port 5555 is already in use`
- Server won't start

**Solutions:**

**Option 1: Find and stop the process using port 5555**

**On Windows:**
```bash
netstat -ano | findstr :5555
```
Find the PID (last number), then:
```bash
taskkill /PID <PID_NUMBER> /F
```

**On Mac/Linux:**
```bash
lsof -ti:5555 | xargs kill -9
```

**Option 2: Use a different port (not recommended for testing)**
- Contact the development team for guidance

---

### Problem: "npm: command not found"

**Symptoms:**
- Terminal says: `npm: command not found`
- Cannot run npm commands

**Solutions:**
1. **Verify Node.js is installed:**
   ```bash
   node --version
   ```
   If this also fails, install Node.js from https://nodejs.org/

2. **Restart your terminal** after installing Node.js

3. **Check PATH environment variable** (advanced users only)

---

### Problem: "Cannot find module" errors

**Symptoms:**
- Errors like: `Cannot find module 'react'` or `Cannot find module 'vite'`
- Server won't start

**Solutions:**
1. **Reinstall dependencies:**
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```
   *(On Windows, use `rmdir /s node_modules` and `del package-lock.json`)*

2. **Clear npm cache:**
   ```bash
   npm cache clean --force
   npm install
   ```

---

### Problem: Browser shows blank page

**Symptoms:**
- Browser loads but shows blank/white page
- No errors visible on page

**Solutions:**
1. **Check browser console:**
   - Press `F12` to open Developer Tools
   - Click "Console" tab
   - Look for red error messages
   - Take a screenshot and share with development team

2. **Try a different browser:**
   - Chrome, Firefox, Safari, Edge
   - Some browsers may have compatibility issues

3. **Clear browser cache:**
   - Press `Ctrl + Shift + Delete` (Windows/Linux) or `Cmd + Shift + Delete` (Mac)
   - Clear cached images and files
   - Reload page (`Ctrl + R` or `Cmd + R`)

---

### Problem: "Network request failed" or API errors

**Symptoms:**
- Search doesn't return results
- Error messages about API calls

**Solutions:**
1. **Check internet connection:**
   - Try visiting other websites
   - The app needs internet to fetch Pokemon card data

2. **Check if API is accessible:**
   - Visit: https://api.pokemontcg.io/v2/cards?page=1&pageSize=1
   - Should return JSON data
   - If blocked, contact IT/network admin

---

### Problem: Slow performance or freezing

**Symptoms:**
- Application is very slow
- Browser freezes when searching

**Solutions:**
1. **Check system resources:**
   - Close other applications
   - Check CPU/memory usage

2. **Try simpler search queries:**
   - Instead of "Charizard", try "Pikachu"
   - Some searches return many results

3. **Check terminal for errors:**
   - Look for error messages in the terminal running the server

---

## 📞 Getting Help

If you encounter issues not covered in this guide:

1. **Check the terminal output** - Copy any error messages
2. **Check the browser console** (F12 → Console tab) - Take screenshots
3. **Document what you were doing** when the error occurred
4. **Contact the development team** with:
   - Error messages (full text)
   - Screenshots
   - Steps you took before the error
   - Your operating system and browser version

---

## 📝 Quick Reference Commands

**Start the server:**
```bash
npm run frontend:5555
```

**Stop the server:**
```
Press Ctrl+C (or Cmd+C on Mac)
```

**Check if server is running:**
- Visit: `http://localhost:5555` in browser
- OR check terminal for "ready" message

**Reinstall dependencies:**
```bash
npm install
```

**Check Node.js version:**
```bash
node --version
```

**Check npm version:**
```bash
npm --version
```

---

## 🌐 Remote Access (Codespaces/WSL/Remote Server)

If you're testing on a remote machine:

### GitHub Codespaces

1. **Start the server** (same as above)
2. **Look for the forwarded URL** in the terminal or Codespaces panel
3. **It will look like:** `https://your-codespace-name-5555.app.github.dev`
4. **Click the URL** or copy-paste into browser
5. ✅ The application should load

### WSL (Windows Subsystem for Linux)

1. **Start the server** in WSL terminal
2. **Access from Windows browser:**
   - Use: `http://localhost:5555`
   - OR: `http://127.0.0.1:5555`
3. **If localhost doesn't work:**
   - Find WSL IP: `ip addr show eth0` (in WSL)
   - Use that IP: `http://<WSL_IP>:5555`

### Remote Server (SSH)

1. **Start the server** on remote machine
2. **Set up port forwarding** (if needed):
   ```bash
   ssh -L 5555:localhost:5555 user@remote-server
   ```
3. **Access from local browser:**
   - Use: `http://localhost:5555`

---

## ✅ Success Indicators

You'll know everything is working correctly when:

- ✅ Terminal shows: `VITE v7.x.x ready in XXX ms`
- ✅ Terminal shows: `Local: http://localhost:5555/`
- ✅ Browser loads the Pokemon TCG Search page
- ✅ Search functionality works
- ✅ Cards display correctly
- ✅ No errors in browser console (F12)
- ✅ No errors in terminal

---

## 📚 Additional Resources

- **Project README:** `/README.md`
- **Frontend Ports Guide:** `/documentation/FRONTEND_PORTS.md`
- **Development Ports Guide:** `/documentation/DEV_PORTS_GUIDE.md`
- **Main Project Documentation:** `/documentation/README.md`

---

## 🎉 You're All Set!

Once you see the application running in your browser, you're ready to start testing!

**Remember:**
- Keep the terminal window open while testing
- Use `Ctrl+C` to stop the server when done
- Report any issues to the development team

**Happy Testing! 🧪✨**

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Maintained By:** Development Team
