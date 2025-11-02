# GitHub Codespaces - Front-End URLs Reference

**Date:** November 1, 2025  
**Repository:** joesuuf/pokemon-dev  
**Branch:** critical-performance-fixes  
**Status:** ? All servers running

---

## ?? Codespaces URLs

### How to Access Your Codespaces URLs

GitHub Codespaces automatically creates forwarded URLs for your ports. You can find them in:

1. **Codespaces Ports Tab** (Recommended)
   - In VS Code: Click "Ports" tab at the bottom
   - Or: Click the "Ports" button in the terminal
   - You'll see all forwarded ports with their URLs

2. **Or Use This Format:**
   - Codespaces typically uses: `https://<CODESPACE_NAME>-<PORT>.github.dev`
   - Or: `https://<CODESPACE_NAME>-<PORT>.preview.app.github.dev`

---

## ?? Port Configuration

### Port 6666 - React 19 (Latest Features)
- **Local URL:** http://localhost:6666
- **Codespaces URL:** See Ports tab or use format above
- **Status:** ? Running (Vite dev server)
- **Description:** React 19 with latest features, primary development server
- **Features:** Hot Module Replacement (HMR), Fast Refresh

### Port 8888 - React Main (Vite Dev Server)
- **Local URL:** http://localhost:8888
- **Codespaces URL:** See Ports tab or use format above
- **Status:** ? Running (Vite dev server)
- **Description:** Main React development server with hot reload
- **Features:** Hot Module Replacement (HMR), Fast Refresh

### Port 9999 - Pure HTML/CSS/JS v2
- **Local URL:** http://localhost:9999
- **Codespaces URL:** See Ports tab or use format above
- **Status:** ? Running (http-server)
- **Description:** Pure HTML/CSS/JavaScript version (no frameworks)
- **Features:** Static file serving, no build step required

### Port 7777 - Carousel Demo
- **Local URL:** http://localhost:7777
- **Codespaces URL:** See Ports tab or use format above
- **Status:** ? Running (http-server)
- **Description:** Carousel front-end demo showcase
- **Features:** Single-file HTML app, inline styles

---

## ?? Finding Your Codespaces URLs

### Method 1: VS Code Ports Tab (Easiest)

1. Open VS Code in your Codespace
2. Click the **"Ports"** tab at the bottom of the screen
3. You'll see a list like:
   ```
   Port    Status    Label              URL
   6666   Forwarded  React 19           https://your-codespace-6666.github.dev
   8888   Forwarded  React Main         https://your-codespace-8888.github.dev
   9999   Forwarded  Pure HTML v2        https://your-codespace-9999.github.dev
   7777   Forwarded  Carousel           https://your-codespace-7777.github.dev
   ```
4. Click the **"Copy"** icon next to each URL or click the **globe icon** to open in browser

### Method 2: Terminal Command

Run this command to see forwarded ports:
```bash
# Check if ports are forwarded
gh codespace ports list
```

### Method 3: Codespaces Web UI

1. Go to: https://github.com/codespaces
2. Click on your active codespace
3. Go to **"Ports"** tab
4. You'll see all forwarded ports with their URLs

---

## ?? URLs to Save

Once you find your Codespaces URLs from the Ports tab, save them here:

### React 19 (Port 6666)
```
URL: https://_________________-6666.github.dev
or:  https://_________________-6666.preview.app.github.dev
```

### React Main (Port 8888)
```
URL: https://_________________-8888.github.dev
or:  https://_________________-8888.preview.app.github.dev
```

### Pure HTML v2 (Port 9999)
```
URL: https://_________________-9999.github.dev
or:  https://_________________-9999.preview.app.github.dev
```

### Carousel (Port 7777)
```
URL: https://_________________-7777.github.dev
or:  https://_________________-7777.preview.app.github.dev
```

---

## ?? Port Forwarding Status

All ports are configured to bind to `0.0.0.0` (all interfaces), which means:
- ? Ports are accessible from Codespaces
- ? Ports should auto-forward in Codespaces
- ? Ports are accessible via localhost (for SSH port forwarding)

**Current Port Status:**
- ? Port 6666: LISTENING on 0.0.0.0:6666
- ? Port 8888: LISTENING on 0.0.0.0:8888
- ? Port 9999: LISTENING on 0.0.0.0:9999
- ? Port 7777: LISTENING on 0.0.0.0:7777

---

## ?? Quick Access

### If Ports Are Already Forwarded:

1. **Check VS Code Ports Tab:**
   - Look for ports 6666, 7777, 8888, 9999
   - Copy the URLs shown there

2. **Or Check GitHub Web UI:**
   - Go to your Codespace in GitHub
   - Open the "Ports" tab
   - Copy the public URLs

### If Ports Need Forwarding:

1. **In VS Code:**
   - Open Ports tab
   - Click "Forward a Port"
   - Enter port number (6666, 8888, 9999, or 7777)
   - Set visibility to "Public" if you want shareable URLs

2. **Or Use GitHub CLI:**
   ```bash
   gh codespace ports forward 6666 --visibility public
   gh codespace ports forward 8888 --visibility public
   gh codespace ports forward 9999 --visibility public
   gh codespace ports forward 7777 --visibility public
   ```

---

## ?? Mobile/Remote Access

If you've set ports to "Public" visibility, you can:
- ? Access from any device (phone, tablet, etc.)
- ? Share URLs with team members
- ? Access from anywhere with internet

**Note:** Public URLs are secure - they require authentication through GitHub.

---

## ?? Security Note

- **Private Ports:** Only accessible to you
- **Public Ports:** Accessible to anyone with the URL (requires GitHub auth)
- **Recommended:** Use Private for development, Public for sharing/demos

---

## ?? Pro Tips

1. **Bookmark URLs:** Once you have the Codespaces URLs, bookmark them for quick access
2. **Set to Public:** For easier access, set ports to "Public" visibility
3. **Use Ports Tab:** The VS Code Ports tab is the easiest way to manage URLs
4. **Share URLs:** Public URLs can be shared with team members for testing

---

## ?? Troubleshooting

### If URLs Don't Work:

1. **Check Port Status:**
   ```bash
   # Verify servers are running
   curl http://localhost:6666
   curl http://localhost:8888
   curl http://localhost:9999
   curl http://localhost:7777
   ```

2. **Check Port Forwarding:**
   - Open VS Code Ports tab
   - Ensure ports are forwarded
   - Try "Forward a Port" if not visible

3. **Restart Servers if Needed:**
   ```bash
   # Servers should already be running, but if not:
   npm run dev:6666    # Port 6666
   npm run dev         # Port 8888
   npm run v2:serve    # Port 9999
   npm run carousel:serve  # Port 7777
   ```

---

## ?? Quick Reference

**Repository:** joesuuf/pokemon-dev  
**Branch:** critical-performance-fixes  
**All Servers:** ? Running  
**Ports:** 6666, 7777, 8888, 9999  
**Status:** Ready for access

**To Get Your URLs:**
1. Open VS Code Ports tab
2. Copy the URLs shown for each port
3. Save them for future reference

---

**Last Updated:** November 1, 2025  
**Next Steps:** Check VS Code Ports tab for your actual Codespaces URLs and save them above!
