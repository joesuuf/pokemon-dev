# Dead Code Detection

## Overview

The Mobile Security & Standards Agent includes intelligent **dead code detection** to identify unused and outdated files in your codebase. This feature helps maintain a clean, maintainable codebase by finding files that are no longer needed.

## Features

### 🔍 Detection Methods

The agent uses multiple heuristics to identify potentially unused files:

1. **Reference Analysis**: Scans all files for imports and references
2. **Naming Patterns**: Detects deprecated naming conventions
3. **File Extensions**: Identifies backup and temporary files
4. **Duplicate Detection**: Finds similar files that may be redundant
5. **File Size Analysis**: Flags empty or nearly-empty files
6. **Framework Detection**: Identifies legacy framework files (e.g., Svelte in React projects)

### 📊 Confidence Levels

Files are categorized by confidence level:

- **🔴 High Confidence**: Very likely unused (0 references, deprecated naming, backup extensions)
- **🟡 Medium Confidence**: Possibly unused (few references, similar files exist)
- **🟢 Low Confidence**: May be unused (requires manual review)

### 📄 Reports Generated

The agent automatically generates a detailed Markdown report (`unused-files-*.md`) containing:

- Summary of files by confidence level
- Detailed information for each file:
  - File path
  - Reason for flagging
  - Number of references found
  - File size and last modified date
  - Suggested action
- Step-by-step removal process
- Commands for testing file removal

## Usage

### Running Dead Code Detection

Dead code detection runs automatically with every security scan:

```bash
# Run full scan (includes dead code detection)
./security-agent/run-agent.sh

# Or via npm
npm run security:scan
```

### Disabling Dead Code Detection

Edit `security-agent/config/agent-config.json`:

```json
{
  "deadCode": {
    "enabled": false
  }
}
```

## Detection Criteria

### Criteria 1: No References Found

**Confidence: HIGH**

Files with zero imports or references across the entire codebase:

```typescript
// No file imports this component
import { OldComponent } from './OldComponent';
```

### Criteria 2: Deprecated Naming Patterns

**Confidence: HIGH/MEDIUM**

Files with names suggesting they're outdated:

- `*-old.*` (e.g., `Button-old.tsx`)
- `*-backup.*` (e.g., `api-backup.js`)
- `*-copy.*` (e.g., `utils-copy.ts`)
- `*-temp.*` (e.g., `test-temp.js`)
- `*deprecated*` (e.g., `deprecated-service.ts`)

### Criteria 3: Underscore Prefix

**Confidence: HIGH**

Files already marked with underscore (staged for removal):

- `_OldComponent.tsx`
- `_backup-file.js`

### Criteria 4: Duplicate Files

**Confidence: MEDIUM**

Similar files that may be redundant:

- `Button.tsx` and `Button2.tsx`
- `api.ts` and `api-old.ts`

### Criteria 5: Empty or Nearly Empty

**Confidence: MEDIUM**

Files smaller than 100 bytes (configurable):

- Placeholder files
- Abandoned stubs
- Empty test files

### Criteria 6: Backup File Extensions

**Confidence: HIGH**

Files with backup/temporary extensions:

- `.old`, `.bak`, `.backup`, `.tmp`
- Example: `config.json.old`

### Criteria 7: Legacy Framework Files

**Confidence: MEDIUM**

Framework files that don't match current project:

- `.svelte` files in React projects
- `.vue` files in React projects
- Class components in hooks-only projects

## Workflow: Safe File Removal

### Step 1: Review the Report

After scanning, open the generated report:

```bash
# Report location
security-agent/reports/unused-files-YYYYMMDD_HHMMSS.md
```

Review each file, paying attention to:
- Confidence level
- Reason for flagging
- Number of references
- Last modified date

### Step 2: Rename Files with Underscore

To safely test if a file is unused, rename it with an underscore prefix:

```bash
# Rename a single file
mv src/components/OldComponent.tsx src/components/_OldComponent.tsx

# Or use git mv to track the rename
git mv src/components/OldComponent.tsx src/components/_OldComponent.tsx
```

**Why underscore?**
- Makes the file "invisible" to most import systems
- Easy to identify staged-for-removal files
- Easy to revert if needed

### Step 3: Test Your Application

After renaming files, thoroughly test your application:

```bash
# Start development server
npm run dev

# Check for errors in console
# Look for import errors like:
# "Cannot find module './OldComponent'"

# Run test suite
npm run test

# Run build
npm run build

# Test all major features manually
```

### Step 4: Monitor for Issues

Keep the renamed files for at least a few days:

- Monitor production logs (if deployed to staging)
- Check user reports
- Run through all user flows
- Test edge cases

### Step 5: Delete Confirmed Unused Files

If no issues arise, safely delete the files:

```bash
# Delete the file
rm src/components/_OldComponent.tsx

# Or with git
git rm src/components/_OldComponent.tsx
git commit -m "Remove unused component: OldComponent"
```

## Configuration

### Enable/Disable Detection Methods

Edit `security-agent/config/agent-config.json`:

```json
{
  "deadCode": {
    "enabled": true,
    "detection": {
      "checkReferences": true,        // Scan for imports/references
      "checkFileAge": false,           // Check last modified date
      "checkFileSize": true,           // Flag empty files
      "checkNamingPatterns": true,     // Look for deprecated names
      "checkDuplicates": true,         // Find similar files
      "checkFileExtensions": true      // Check for .old, .bak, etc.
    },
    "patterns": {
      "deprecated": ["old", "backup", "deprecated", "temp", "copy"],
      "backupExtensions": [".old", ".bak", ".backup", ".tmp"],
      "emptyFileThreshold": 100
    }
  }
}
```

### Adjust Empty File Threshold

Change the size threshold for flagging empty files:

```json
{
  "deadCode": {
    "patterns": {
      "emptyFileThreshold": 50  // Flag files smaller than 50 bytes
    }
  }
}
```

### Add Custom Deprecated Patterns

Add your own naming patterns to detect:

```json
{
  "deadCode": {
    "patterns": {
      "deprecated": [
        "old",
        "backup",
        "legacy",
        "archive",
        "unused",
        "TODO-delete"
      ]
    }
  }
}
```

## Example Report

```markdown
# Unused & Outdated Files Report

**Generated:** 2025-10-31T15:30:00

**Total Files Found:** 8

---

## Summary

- **High Confidence:** 5 files
- **Medium Confidence:** 2 files
- **Low Confidence:** 1 file

## 🔴 High Confidence (Likely Unused)

### `src/components/LoadingSpinner.svelte`

**Confidence:** HIGH

**Reason:** Svelte component in React project (legacy code); No imports or references found in codebase

**Details:**
- References found: 0
- File size: 2456 bytes
- Last modified: 2024-08-15T10:23:45

**Suggested Action:** Rename with underscore prefix to verify, then delete if no issues arise

---

### `src/utils/old-helpers.ts`

**Confidence:** HIGH

**Reason:** Filename suggests deprecated/backup code: 'old-helpers.ts'; No imports or references found in codebase

**Details:**
- References found: 0
- File size: 1024 bytes
- Last modified: 2024-06-20T14:30:00

**Suggested Action:** Rename with underscore prefix to verify, then delete if no issues arise

---
```

## Best Practices

### 1. Review Before Deleting

**Never blindly delete files** based solely on the report. Always:
- Review the reason
- Check the confidence level
- Consider the last modified date
- Look for special cases (config files, types, etc.)

### 2. Use Version Control

Always use git when removing files:

```bash
# Good: Tracked deletion
git rm unused-file.ts
git commit -m "Remove unused file"

# If you need to recover:
git checkout HEAD~1 -- unused-file.ts
```

### 3. Delete in Batches

Don't delete all files at once:

1. Start with high-confidence files
2. Delete 3-5 files at a time
3. Test thoroughly between batches
4. Deploy to staging before production

### 4. Document Why

Add context to your commit messages:

```bash
git commit -m "Remove unused Svelte components

These components are from the old Svelte implementation
and are no longer used since migrating to React.

Tested:
- Full test suite passes
- Manual testing of all features
- No console errors"
```

### 5. Keep a Backup Branch

Before major cleanup:

```bash
git checkout -b backup/pre-cleanup
git checkout main
# Do cleanup
```

## Common Scenarios

### Scenario 1: Type Definition Files

**Issue:** Type files may have 0 import references but are still needed.

**Solution:**
- Check if used in `tsconfig.json` `types` array
- Look for `/// <reference types="..." />` comments
- Consider if it's a global type definition

### Scenario 2: Entry Point Files

**Issue:** Files like `index.ts` may show few references.

**Solution:**
- Check `package.json` `main` or `exports` fields
- Look for bundler entry points in `vite.config.ts`, `webpack.config.js`
- Verify it's not a public API entry point

### Scenario 3: Test Files

**Issue:** Test files may not be imported by other files.

**Solution:**
- Test files are consumed by test runners, not imported
- Check if still testing active code
- Consider test coverage impact

### Scenario 4: Config Files

**Issue:** Config files often have 0 import references.

**Solution:**
- Config files are consumed by tools, not imports
- Check documentation for required configs
- Verify with tool's docs before removing

## Troubleshooting

### False Positives

If you get false positives:

1. **Dynamic imports:**
   ```typescript
   // May not be detected
   const module = await import(`./modules/${name}.ts`);
   ```

2. **String-based references:**
   ```typescript
   // May not be detected
   require.context('./components', true, /\.tsx$/);
   ```

3. **External tools:**
   - Files used by build tools
   - Files loaded by test runners
   - Files referenced in config

**Solution:** Add these files to exclude patterns in config

### File Still Needed After Deletion

If you deleted a file too early:

```bash
# Recover from git
git log --all --full-history -- path/to/file
git checkout <commit-hash> -- path/to/file

# Or from reflog
git reflog
git checkout HEAD@{n} -- path/to/file
```

## Integration with CI/CD

### Prevent Committing Underscore Files

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for underscore-prefixed files
UNDERSCORE_FILES=$(git diff --cached --name-only | grep '/\_[^/]*\.')

if [ -n "$UNDERSCORE_FILES" ]; then
    echo "Error: Cannot commit files marked for removal (underscore prefix):"
    echo "$UNDERSCORE_FILES"
    echo ""
    echo "Either delete these files or remove the underscore prefix."
    exit 1
fi
```

### Weekly Dead Code Reports

Add to `.github/workflows/dead-code-report.yml`:

```yaml
name: Weekly Dead Code Report

on:
  schedule:
    - cron: '0 9 * * MON'  # Every Monday at 9 AM

jobs:
  dead-code-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run Dead Code Detection
        run: python3 security-agent/agent.py

      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: unused-files-report
          path: security-agent/reports/unused-files-*.md
```

## Metrics and Goals

Track your dead code removal progress:

```bash
# Count underscore-prefixed files (staged for removal)
find . -name '_*' -type f | wc -l

# Count .old/.bak files
find . -name '*.old' -o -name '*.bak' | wc -l

# Lines of code trend
cloc --by-file . > cloc-$(date +%Y%m%d).txt
```

Set goals:
- Remove 10 files per sprint
- Zero .old/.bak files
- < 5% dead code ratio

## Support

For issues or questions about dead code detection:
- Check the generated report for detailed explanations
- Review this documentation
- Open an issue on GitHub

## See Also

- [Main README](../README.md)
- [Security Agent Documentation](./README.md)
- [Configuration Guide](./config/agent-config.json)
