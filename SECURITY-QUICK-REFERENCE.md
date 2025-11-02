# Security Quick Reference Guide
**Hiding and Protecting Sensitive Items**

---

## 🔐 Quick Security Checklist

Before committing any code, verify:

- [ ] No API keys in source code
- [ ] No passwords or credentials in files
- [ ] `.env` files are in `.gitignore`
- [ ] No sensitive data in console.log statements
- [ ] Environment variables don't start with `VITE_` (unless meant to be public)
- [ ] No hardcoded URLs with tokens/keys in query params

---

## 📁 Files That Should NEVER Be Committed

```
.env
.env.local
.env.production
.env.staging
secrets.json
credentials.json
*.key
*.pem
*.p12
*.pfx
config/secrets.js
**/*secret*
**/*password*
**/*credential*
```

### Update Your .gitignore

```bash
# Environment variables
.env
.env.local
.env.*.local
.env.production
.env.staging

# Secrets
secrets/
*.secret
*secret*.json
credentials/
*.key
*.pem
*.cert

# Logs (may contain sensitive data)
logs/
*.log
npm-debug.log*

# OS Files
.DS_Store
Thumbs.db
```

---

## 🔑 Safe API Key Management

### ❌ NEVER Do This (Frontend)
```typescript
// BAD: Exposes key to browser
const API_KEY = "f43ae006-2449-4771-8442-a17179cacbdf";
const API_KEY = import.meta.env.VITE_API_KEY; // VITE_ prefix = exposed!
```

### ✅ Always Do This

**Backend (Secure):**
```typescript
// GOOD: Server-side only
const API_KEY = process.env.API_KEY; // No VITE_ prefix!
```

**Frontend (Use Proxy):**
```typescript
// GOOD: No API key needed, use backend proxy
const response = await fetch('/api/cards?q=pikachu');
```

---

## 🌐 Environment Variables Guide

### Vite Environment Variables

**Rule:** Any variable starting with `VITE_` is exposed to the browser!

```bash
# ❌ INSECURE - Bundled into JavaScript
VITE_API_KEY=secret123
VITE_DATABASE_URL=postgresql://...

# ✅ SECURE - Only available server-side
API_KEY=secret123
DATABASE_URL=postgresql://...

# ✅ OK - Public information
VITE_APP_VERSION=1.0.0
VITE_PUBLIC_URL=https://example.com
```

### Setting Environment Variables

**Development (.env file):**
```bash
# .env (NOT committed to git)
API_KEY=your-secret-key-here
DATABASE_URL=postgresql://localhost/mydb
```

**Production (Vercel):**
1. Go to Vercel Dashboard
2. Select your project
3. Settings → Environment Variables
4. Add variables (they stay on server, never exposed)

**Accessing in Code:**
```typescript
// Backend/Server-side
const apiKey = process.env.API_KEY;

// Frontend (only if using backend API)
const response = await fetch('/api/endpoint'); // No key needed
```

---

## 🛡️ Hiding Secrets That Were Already Committed

### Step 1: Rotate the Secret
**FIRST and MOST IMPORTANT:** Change the compromised secret immediately!
- API keys: Revoke old key, generate new one
- Passwords: Change them
- Tokens: Generate new ones

### Step 2: Remove from Git Tracking
```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### Step 3: Remove from Git History

**Option A: Using BFG Repo-Cleaner (Easiest)**
```bash
# Download from https://rtyley.github.io/bfg-repo-cleaner/
java -jar bfg.jar --delete-files .env
java -jar bfg.jar --replace-text passwords.txt  # File with text to replace

cd your-repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

**Option B: Using git filter-branch**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push --force --all
```

**Option C: Using git filter-repo (Recommended by Git)**
```bash
# Install: pip install git-filter-repo
git filter-repo --path .env --invert-paths
git push --force --all
```

### Step 4: Notify Your Team
After force pushing:
```
⚠️ IMPORTANT: Git history has been rewritten!
All team members must:
1. Back up any uncommitted changes
2. Delete their local repository
3. Re-clone from the remote
   git clone <repository-url>
```

---

## 🔍 Finding Exposed Secrets

### Scan Your Codebase
```bash
# Search for potential API keys
grep -r "api[_-]key" --include="*.js" --include="*.ts" .

# Search for passwords
grep -r "password\s*=" --include="*.js" --include="*.ts" .

# Search for common secret patterns
grep -r "['\"][a-zA-Z0-9]{32,}['\"]" --include="*.js" --include="*.ts" .

# Search git history for .env
git log --all --full-history --source --all -- .env

# Search all commits for a specific secret
git grep "secret-value-here" $(git rev-list --all)
```

### Automated Tools
```bash
# Install truffleHog (finds secrets in git)
pip install truffleHog
truffleHog --regex --entropy=True .

# Install GitGuardian CLI
npm install -g @gitguardian/ggshield
ggshield scan repo .

# Use gitleaks
docker run -v "$(pwd)":/path zricethezav/gitleaks:latest detect --source="/path"
```

---

## 🔐 Secure Coding Patterns

### API Keys
```typescript
// ❌ BAD
const apiKey = "sk_live_abc123xyz789";
fetch(`https://api.example.com?key=${apiKey}`);

// ✅ GOOD
// Backend only!
const apiKey = process.env.API_KEY;
fetch('https://api.example.com', {
  headers: { 'Authorization': `Bearer ${apiKey}` }
});
```

### Database Credentials
```typescript
// ❌ BAD
const db = connect({
  host: 'db.example.com',
  user: 'admin',
  password: 'password123'
});

// ✅ GOOD
const db = connect({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD
});
```

### OAuth Tokens
```typescript
// ❌ BAD
localStorage.setItem('token', 'eyJhbGc...');

// ✅ GOOD - Use httpOnly cookies (backend sets them)
// Frontend doesn't handle tokens directly
// Or use secure token storage like secure cookie with SameSite
```

---

## 🚨 What To Do If You Accidentally Committed Secrets

1. **STOP** - Don't panic, but act quickly
2. **ROTATE** - Immediately change/revoke the exposed secret
3. **REMOVE** - Remove from git tracking (`git rm --cached`)
4. **CLEAN** - Clean git history (use BFG or filter-branch)
5. **VERIFY** - Search git history to ensure it's gone
6. **NOTIFY** - Tell your team about the force push
7. **AUDIT** - Check if the secret was used maliciously
8. **LEARN** - Set up pre-commit hooks to prevent future leaks

---

## 🔒 Prevention: Pre-commit Hooks

### Install git-secrets
```bash
# macOS
brew install git-secrets

# Other OS
git clone https://github.com/awslabs/git-secrets
cd git-secrets
make install

# Set up in your repo
cd /path/to/your/repo
git secrets --install
git secrets --register-aws
```

### Create .git/hooks/pre-commit
```bash
#!/bin/bash

# Check for .env files
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "❌ Error: Attempting to commit .env file!"
    echo "Please remove it from the commit."
    exit 1
fi

# Check for potential API keys
if git diff --cached | grep -qE "['\"][a-zA-Z0-9]{32,}['\"]"; then
    echo "⚠️  Warning: Potential API key detected!"
    echo "Please verify you're not committing secrets."
    exit 1
fi

# Check for VITE_ variables in .env
if git diff --cached | grep -q "VITE_.*=.*[a-zA-Z0-9]{20,}"; then
    echo "⚠️  Warning: VITE_ prefix detected with long value!"
    echo "Remember: VITE_ variables are exposed to the browser!"
    exit 1
fi

exit 0
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 📋 Security Incident Response Plan

If a secret is exposed:

**Hour 1 (Immediate):**
- [ ] Rotate/revoke the compromised secret
- [ ] Check logs for unauthorized usage
- [ ] Assess the scope of exposure

**Hours 2-4 (Containment):**
- [ ] Remove secret from git tracking
- [ ] Clean git history
- [ ] Force push changes
- [ ] Notify team members

**Days 2-7 (Recovery):**
- [ ] Audit for any damage
- [ ] Implement pre-commit hooks
- [ ] Update documentation
- [ ] Train team on secure practices

**Ongoing:**
- [ ] Monitor for unusual activity
- [ ] Regular security audits
- [ ] Keep secrets rotation schedule

---

## 🛠️ Tools & Resources

### Secret Management Tools
- **Vercel Environment Variables** (for this project)
- **AWS Secrets Manager**
- **HashiCorp Vault**
- **Azure Key Vault**
- **Google Cloud Secret Manager**

### Secret Scanning Tools
- **TruffleHog** - Find secrets in git history
- **GitGuardian** - Real-time secret detection
- **Gitleaks** - SAST tool for secrets
- **git-secrets** - Prevents committing secrets

### Learning Resources
- [OWASP Secret Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)

---

## ✅ Final Checklist

Before every commit:
- [ ] No hardcoded secrets in code
- [ ] All `.env` files in `.gitignore`
- [ ] Environment variables properly prefixed (no `VITE_` for secrets)
- [ ] Secrets stored in environment variables or secret manager
- [ ] No sensitive data in logs
- [ ] Pre-commit hooks enabled

Before every deployment:
- [ ] Verify production secrets are rotated regularly
- [ ] Check that all environment variables are set in deployment platform
- [ ] Audit logs for suspicious activity
- [ ] Test that no secrets are exposed in browser console or network tab

---

## 🆘 Emergency Commands

```bash
# Remove file from latest commit (before push)
git reset HEAD~1
git rm --cached .env
git commit -m "Remove .env"

# Amend last commit to remove file (before push)
git rm --cached .env
git commit --amend --no-edit

# Search entire git history for a secret
git log -S "secret-value" --source --all

# Remove all traces of a file from history
git filter-repo --path .env --invert-paths

# Force push after history rewrite (⚠️ WARNING: DESTRUCTIVE)
git push --force --all
git push --force --tags
```

---

**Remember:** The best security is prevention. Always review changes before committing!

