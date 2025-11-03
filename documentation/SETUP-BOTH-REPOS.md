# Setup Guide: Creating PRs for Both Repositories

## Current Status ✅

### pokemon-dev Repository
- ✅ Branch pushed: `claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg`
- ✅ All changes committed and ready
- ✅ Remote configured: `origin`

### pokemon-www-v0.1 Repository
- ⚠️ Repository may need to be created or authorized
- ⚠️ Remote configured but push failed (502 error)
- 📋 Manual setup required (instructions below)

---

## Option 1: pokemon-www-v0.1 Already Exists

If the `pokemon-www-v0.1` repository already exists on GitHub:

### Step 1: Verify Repository Access
```bash
# Check if you can access the repository
gh repo view joesuuf/pokemon-www-v0.1
```

### Step 2: Push Branch to pokemon-www-v0.1
```bash
# Make sure you're on the correct branch
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Push to pokemon-www-v0.1 (retry if needed)
git push -u pokemon-www claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# If that fails, try with HTTPS URL directly:
git push https://github.com/joesuuf/pokemon-www-v0.1.git claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg
```

### Step 3: Create PR on GitHub
Use the PR details from `documentation/process/documentation/process/PR-DETAILS.md`:
- **URL:** https://github.com/joesuuf/pokemon-www-v0.1/pull/new/claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

---

## Option 2: pokemon-www-v0.1 Doesn't Exist Yet

If you need to create the `pokemon-www-v0.1` repository to mirror `pokemon-dev`:

### Step 1: Create the Repository on GitHub

#### Via GitHub CLI:
```bash
gh repo create joesuuf/pokemon-www-v0.1 \
  --public \
  --description "Pokemon TCG Search - Web Version v0.1" \
  --homepage "https://pokemon-www-v0.1.com"
```

#### Via GitHub Web:
1. Go to https://github.com/new
2. Set repository name: `pokemon-www-v0.1`
3. Description: "Pokemon TCG Search - Web Version v0.1"
4. Choose: Public or Private
5. **Do NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### Step 2: Push All Content
```bash
# Remove the old remote if it exists
git remote remove pokemon-www 2>/dev/null || true

# Add the correct remote
git remote add pokemon-www https://github.com/joesuuf/pokemon-www-v0.1.git

# Push all branches (to mirror pokemon-dev)
git push -u pokemon-www --all

# Push tags if any
git push pokemon-www --tags
```

### Step 3: Create PR
Use the PR details from `documentation/process/documentation/process/PR-DETAILS.md`:
- **URL:** https://github.com/joesuuf/pokemon-www-v0.1/pull/new/claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

---

## Option 3: Fork pokemon-dev to pokemon-www-v0.1

If you want `pokemon-www-v0.1` to be a fork or mirror:

### Via GitHub Web:
1. Go to https://github.com/joesuuf/pokemon-dev
2. Click "Fork" button
3. Change the name to `pokemon-www-v0.1`
4. Click "Create fork"

### Then:
```bash
# Clone the fork
cd ~/projects
git clone https://github.com/joesuuf/pokemon-www-v0.1.git
cd pokemon-www-v0.1

# The branch should already be there if it was on pokemon-dev
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Create PR via the fork
```

---

## Creating the Pull Requests

### For pokemon-dev (Ready Now!)

#### Quick Links:
- **Branch:** `claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg`
- **PR URL:** https://github.com/joesuuf/pokemon-dev/pull/new/claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

#### Steps:
1. Go to the PR URL above
2. GitHub will show the comparison
3. Copy the content from `documentation/process/documentation/process/PR-DETAILS.md`
4. Paste into the PR description
5. Click "Create pull request"

### For pokemon-www-v0.1 (After Setup)

#### Quick Links:
- **Branch:** `claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg`
- **PR URL:** https://github.com/joesuuf/pokemon-www-v0.1/pull/new/claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

#### Steps:
1. Complete one of the setup options above
2. Go to the PR URL
3. Copy the content from `documentation/process/documentation/process/PR-DETAILS.md`
4. Paste into the PR description
5. Click "Create pull request"

---

## Using GitHub CLI to Create PRs

If you have `gh` CLI configured:

### For pokemon-dev:
```bash
cd /home/user/pokemon-dev
gh pr create \
  --repo joesuuf/pokemon-dev \
  --title "Implement Tailwind CSS v4.1.16 and Fix TypeScript Errors" \
  --body-file documentation/process/documentation/process/PR-DETAILS.md \
  --head claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg
```

### For pokemon-www-v0.1:
```bash
# First ensure branch is pushed
git push -u pokemon-www claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Then create PR
gh pr create \
  --repo joesuuf/pokemon-www-v0.1 \
  --title "Implement Tailwind CSS v4.1.16 and Fix TypeScript Errors" \
  --body-file documentation/process/documentation/process/PR-DETAILS.md \
  --head claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg
```

---

## Troubleshooting

### Issue: "repository not authorized" or 502 error

**Possible causes:**
- Repository doesn't exist yet
- No push access to the repository
- Wrong repository name
- Network/proxy issues

**Solutions:**
1. Create the repository (see Option 2 above)
2. Check repository permissions
3. Use HTTPS URL instead of local proxy
4. Verify repository name is correct

### Issue: "branch not found"

**Solution:**
```bash
# Make sure you're on the branch
git checkout claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg

# Push with force if needed (be careful!)
git push -u pokemon-www claude/check-tailwind-version-011CUfUBLNqZ6mnFTZtHHSZg --force
```

### Issue: "no base branch"

**Solution:**
- If the repository is new, you may need to push a base branch first (e.g., `main`)
- Or set the default branch in GitHub settings

---

## What's in the PRs

Both PRs will include:

### Commits:
1. `e3ae125` - Merge sandbox implementation
2. `f686c6f` - Implement Tailwind CSS v4.1.16
3. `ccb0e0b` - Add comprehensive documentation
4. `a1da4a1` - Add .gitignore
5. `9177bae` - Add ESLint configuration

### Files Changed:
- `src/lib/types.ts` ← NEW: 213 lines of TypeScript types
- `src/index.css` ← MODIFIED: Added Tailwind import and theme
- `PROJECT-STATUS.md` ← NEW: Project roadmap
- `docs/` ← NEW: Comprehensive documentation
- `requirements.txt` ← NEW: System requirements

### Testing:
- ✅ TypeScript compilation passes
- ✅ Production build succeeds
- ✅ Dev server starts successfully
- ✅ All security checks pass

---

## Summary

### Current State:
- ✅ **pokemon-dev**: Branch pushed, ready for PR
- ⚠️ **pokemon-www-v0.1**: Needs setup (see options above)

### Next Actions:
1. **pokemon-dev**: Create PR using web UI or CLI
2. **pokemon-www-v0.1**: Choose an option above to set up, then create PR

### Files to Reference:
- `documentation/process/documentation/process/PR-DETAILS.md` - Complete PR description
- `PROJECT-STATUS.md` - Project context
- `documentation/guides/tailwind-v4-guide.md` - Technical details

---

## Questions?

If you need help:
1. Check if `pokemon-www-v0.1` exists on GitHub
2. Verify you have push access to both repositories
3. Review error messages carefully
4. Try the alternative methods above

---

**Ready to create PRs!** 🚀
