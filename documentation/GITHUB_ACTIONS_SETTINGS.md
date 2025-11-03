# GitHub Actions Settings Configuration

## ✅ Required Settings for GitHub Pages Deployment

### 1. Actions Permissions
**Recommended:** "Allow all actions and reusable workflows"

**Why:** The workflow uses official GitHub actions:
- `actions/checkout@v4`
- `actions/setup-node@v4`
- `actions/configure-pages@v4`
- `actions/upload-pages-artifact@v3`
- `actions/deploy-pages@v4`

**Alternative:** "Allow joesuuf actions and reusable workflows" should also work since these are official GitHub actions.

### 2. Workflow Permissions
**Required:** "Read and write permissions"

**Why:** The workflow needs:
- `contents: read` - to read repository files
- `pages: write` - to deploy to GitHub Pages ⚠️ CRITICAL
- `id-token: write` - for OIDC authentication

The workflow explicitly sets permissions in `.github/workflows/deploy-dual-github.yml`:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

### 3. Artifact and Log Retention
**Current:** 90 days ✅ (Perfect)

This is fine for keeping deployment logs and artifacts.

### 4. Approval for Fork PRs
**Recommended:** "Require approval for first-time contributors who are new to GitHub"

This provides security while allowing trusted contributors to work.

### 5. GitHub Actions to Create PRs
**Optional:** "Allow GitHub Actions to create and approve pull requests"

Not required for this deployment workflow, but safe to enable if you want automation features.

## ✅ Summary

**Minimum Required Settings:**
1. ✅ Actions permissions: "Allow all actions" OR "Allow joesuuf actions"
2. ✅ Workflow permissions: "Read and write permissions" ⚠️ CRITICAL
3. ✅ Artifact retention: 90 days (already set)

Everything else can be configured based on your security preferences.
