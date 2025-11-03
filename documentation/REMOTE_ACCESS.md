# Remote Access Guide

**Options for accessing the project remotely:**
1. ✅ **GitHub Codespaces** (Recommended - Easiest)
2. 🌐 **Google Cloud Platform (GCP)**
3. 🖥️ **Other Cloud Options**

---

## Option 1: GitHub Codespaces (Recommended)

### Why Codespaces?
- ✅ Already have a paid account
- ✅ Pre-configured environments
- ✅ Integrated with your GitHub repo
- ✅ Browser-based IDE
- ✅ Port forwarding for web servers
- ✅ Free tier available (if needed)

### Setup Steps

1. **Navigate to your repository:**
   ```
   https://github.com/joesuuf/pokemon-dev
   ```

2. **Open in Codespaces:**
   - Click the green **"Code"** button
   - Select **"Codespaces"** tab
   - Click **"Create codespace on main"** (or your branch)
   - Wait for environment to spin up (~2 minutes)

3. **Access your codespace:**
   - Opens in browser automatically
   - Full VS Code interface
   - Integrated terminal

4. **Clone and switch to your branch:**
   ```bash
   git checkout phase1-json-communication
   # Or
   git checkout security-agent-integration
   ```

### Running Servers in Codespaces

**Main Web Server:**
```bash
python3 -m http.server 8000
```

**React Dev Server:**
```bash
npm install  # First time only
npm run dev
```

**Access URLs:**
- Codespaces automatically forwards ports
- Access via: `https://<codespace-name>-8000.app.github.dev`
- Or use the "Ports" tab in VS Code

### Port Forwarding in Codespaces

1. Click **"Ports"** tab (bottom panel)
2. Ports are auto-detected or add manually:
   - Port 8000 → Main web server
   - Port 3000 → React dev server
3. Click **"Public"** to get shareable URL
4. Copy the public URL and share/open in browser

### Terminal Commands in Codespaces

```bash
# Install dependencies
npm install

# Run tests
python -m pytest agents/tests/phase1/ -v

# Start servers
python3 -m http.server 8000 &
npm run dev &

# View schema visualizer
# Access via forwarded port 8000
```

### Codespaces Benefits

- ✅ Pre-installed: Node.js, Python, Git
- ✅ VS Code extensions available
- ✅ Terminal access (bash)
- ✅ File browser
- ✅ Integrated Git
- ✅ Port forwarding (automatic)
- ✅ 4-core machines (paid tier)
- ✅ Persistent storage (until deletion)

### Cost Management

- **Paid tier:** $0.18/hour for 4-core machine
- **Pause:** Codespaces pause after 30 min inactivity (free)
- **Delete:** Delete when not using to avoid charges
- **Monitor:** Check usage at github.com/settings/billing

---

## Option 2: Google Cloud Platform (GCP)

### Setup Cloud VM

1. **Create VM Instance:**
   ```bash
   # Via GCP Console or gcloud CLI
   gcloud compute instances create pokemon-dev \
       --zone=us-central1-a \
       --machine-type=e2-standard-4 \
       --image-family=ubuntu-2204-lts \
       --image-project=ubuntu-os-cloud \
       --boot-disk-size=50GB \
       --tags=http-server,https-server
   ```

2. **SSH into VM:**
   ```bash
   gcloud compute ssh pokemon-dev --zone=us-central1-a
   ```

3. **Install Dependencies:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Install Python (usually pre-installed)
   sudo apt install python3 python3-pip

   # Install Git
   sudo apt install git

   # Install Chrome (for browser testing)
   wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
   sudo apt install ./google-chrome-stable_current_amd64.deb
   ```

4. **Clone Repository:**
   ```bash
   git clone https://github.com/joesuuf/pokemon-dev.git
   cd pokemon-dev
   git checkout phase1-json-communication
   ```

5. **Install Project Dependencies:**
   ```bash
   npm install
   pip3 install jsonschema pytest pytest-cov
   ```

### Access Web Servers from GCP

**Option A: SSH Port Forwarding**
```bash
# From your local machine
gcloud compute ssh pokemon-dev --zone=us-central1-a \
    --ssh-flag="-L 8000:localhost:8000 -L 3000:localhost:3000"

# Then access via:
# http://localhost:8000
# http://localhost:3000
```

**Option B: Firewall Rules + External IP**
```bash
# Add firewall rule
gcloud compute firewall-rules create allow-http-8000 \
    --allow tcp:8000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP on port 8000"

gcloud compute firewall-rules create allow-http-3000 \
    --allow tcp:3000 \
    --source-ranges 0.0.0.0/0 \
    --description "Allow HTTP on port 3000"

# Get external IP
gcloud compute instances describe pokemon-dev \
    --zone=us-central1-a \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)'

# Access via:
# http://<EXTERNAL_IP>:8000
# http://<EXTERNAL_IP>:3000
```

**Option C: Cloud Run (Serverless)**
- Better for production
- More complex setup
- Pay per request

### GCP Setup Script

Create `setup_gcp.sh`:

```bash
#!/bin/bash
set -e

echo "Setting up Pokemon Dev environment on GCP..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python packages
pip3 install jsonschema pytest pytest-cov

# Clone repo
if [ ! -d "pokemon-dev" ]; then
    git clone https://github.com/joesuuf/pokemon-dev.git
    cd pokemon-dev
    git checkout phase1-json-communication
else
    cd pokemon-dev
    git pull
fi

# Install dependencies
npm install

echo "✅ Setup complete!"
echo "Run: python3 -m http.server 8000"
echo "Run: npm run dev"
```

### GCP Cost Considerations

- **e2-standard-4:** ~$0.10/hour (~$73/month if running 24/7)
- **Stop instance when not using:** Saves compute costs (still pay for disk)
- **Preemptible instances:** Much cheaper but can be terminated
- **Cloud Shell:** Free but limited (suitable for quick checks)

---

## Option 3: Quick Remote Access (Codespaces)

### One-Click Access

1. **Bookmark this URL:**
   ```
   https://github.com/codespaces/new?repo=joesuuf/pokemon-dev&branch=phase1-json-communication
   ```

2. **Or use GitHub CLI:**
   ```bash
   gh codespace create --repo joesuuf/pokemon-dev \
       --branch phase1-json-communication \
       --machine premiumLinux32gb
   ```

3. **Open existing codespace:**
   ```
   https://github.com/codespaces
   ```

### Recommended Workflow

1. **Morning:** Create/Resume codespace
2. **Work:** Develop in browser
3. **Evening:** Commit and push changes
4. **Stop:** Let codespace pause automatically

---

## Quick Comparison

| Feature | GitHub Codespaces | GCP VM | GCP Cloud Shell |
|---------|------------------|--------|-----------------|
| **Setup Time** | 2 minutes | 15-30 minutes | Instant |
| **Cost (active)** | $0.18/hr | ~$0.10/hr | Free |
| **Port Forwarding** | Automatic | Manual | Automatic |
| **Persistent Storage** | Yes | Yes | No |
| **Pre-configured** | Yes | No | Yes |
| **Browser-based** | Yes | No (SSH) | Yes |
| **Best for** | Development | Production | Quick checks |

---

## Recommended: GitHub Codespaces

### Why Codespaces?
- ✅ Fastest setup (2 minutes)
- ✅ Pre-configured environment
- ✅ Automatic port forwarding
- ✅ VS Code in browser
- ✅ Integrated with GitHub
- ✅ No SSH configuration needed
- ✅ Easy to start/stop

### Access Steps:

1. **Go to:** https://github.com/joesuuf/pokemon-dev
2. **Click:** Green "Code" button
3. **Select:** "Codespaces" tab
4. **Click:** "Create codespace on phase1-json-communication"
5. **Wait:** ~2 minutes for setup
6. **Open:** Terminal in Codespaces
7. **Run:** Your commands

### Testing in Codespaces:

```bash
# Run tests
python -m pytest agents/tests/phase1/ -v

# View schemas
python3 -m http.server 8000

# Access via forwarded port:
# https://<codespace>-8000.app.github.dev/agents/test-schemas.html

# Start React app
npm run dev

# Access via:
# https://<codespace>-3000.app.github.dev
```

---

## Remote Testing Checklist

### In Codespaces:

- [ ] Clone repository
- [ ] Checkout `phase1-json-communication` branch
- [ ] Install dependencies (`npm install`)
- [ ] Run tests (`python -m pytest agents/tests/phase1/ -v`)
- [ ] Start web server (`python3 -m http.server 8000`)
- [ ] Access via forwarded port URL
- [ ] Start React dev server (`npm run dev`)
- [ ] Access via forwarded port URL
- [ ] View schema visualizer
- [ ] Test HTML front-end

### Files to Review:

- `agents/test-schemas.html` - Schema visualizer
- `index-test.html` - Testing hub
- `v2/index.html` - HTML front-end
- `agents/PHASE1_COMPLETE.md` - Documentation
- `FRONTEND_TESTING_REPORT.md` - Front-end docs
- `documentation/guides/documentation/guides/WSL_SETUP.md` - WSL troubleshooting
- `documentation/guides/documentation/guides/WSL_DEV_RUNNER.md` - Dev runner guide

---

## Quick Start Commands (Codespaces)

```bash
# 1. Clone and checkout branch
git checkout phase1-json-communication

# 2. Install dependencies
npm install
pip3 install jsonschema pytest pytest-cov

# 3. Run tests
python -m pytest agents/tests/phase1/ -v

# 4. Start servers
python3 -m http.server 8000 &
npm run dev &

# 5. Access via Ports tab
# - Click "Ports" tab in VS Code
# - Ports are auto-forwarded
# - Click "Public" to get shareable URL
```

---

## Need Help?

- **Codespaces Docs:** https://docs.github.com/en/codespaces
- **GCP Compute Docs:** https://cloud.google.com/compute/docs
- **Project README:** See `README.md`
- **Phase 1 Docs:** See `agents/PHASE1_COMPLETE.md`

---

**Best Option:** GitHub Codespaces (fastest, easiest, pre-configured)
