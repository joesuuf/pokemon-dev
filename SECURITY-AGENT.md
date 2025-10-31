# Mobile Security & Standardization Agent

## Quick Start

```bash
# Run security scan
./security-agent/run-agent.sh

# Or via npm
npm run security:scan

# For CI/CD (fails on critical issues)
npm run security:ci
```

## What is This?

The **Mobile Security & Standards Agent** is an intelligent security analysis tool that:

1. 🔒 **Detects Mobile Browser Attack Vectors**
   - Cross-Site Scripting (XSS)
   - Injection attacks (SQL, code, command)
   - CSRF vulnerabilities
   - Insecure storage patterns
   - API key exposure
   - CORS misconfigurations
   - And 20+ more security checks

2. 📋 **Enforces Framework Standards**
   - **TypeScript/React**: Component patterns, type safety, security best practices
   - **Python 3**: Type hints, docstrings, PEP 8, security patterns
   - **HTML/CSS v2**: Pure web standards, accessibility, mobile-first

3. 📊 **Generates Comprehensive Reports**
   - JSON (machine-readable for CI/CD)
   - HTML (interactive visual reports)
   - Markdown (human-readable documentation)

## Architecture

```
pokemon-dev/
├── security-agent/
│   ├── agent.py                    # Main security scanner (Python 3)
│   ├── run-agent.sh                # Shell runner script
│   ├── config/
│   │   └── agent-config.json       # Configuration
│   ├── reports/                    # Generated reports (gitignored)
│   │   ├── security-report-*.json
│   │   ├── security-report-*.html
│   │   └── security-report-*.md
│   └── README.md                   # Full documentation
├── v2/                             # Pure HTML/CSS/JS version
│   ├── index.html                  # Secure, accessible HTML
│   ├── styles/                     # Mobile-first CSS
│   ├── scripts/                    # Vanilla JavaScript
│   └── README.md                   # v2 documentation
└── src/                            # React/TypeScript version (v1)
```

## Security Checks Overview

### Critical Severity 🔴

| Check | Description | CWE |
|-------|-------------|-----|
| **XSS** | Detects `dangerouslySetInnerHTML`, `innerHTML`, `eval` | CWE-79 |
| **Injection** | SQL, command, code injection patterns | CWE-89, CWE-95 |
| **CSRF** | Missing CSRF tokens in forms | CWE-352 |
| **Data Exposure** | Hardcoded API keys, passwords, secrets | CWE-798 |

### High Severity 🟠

| Check | Description | CWE |
|-------|-------------|-----|
| **CORS** | Wildcard origins, permissive policies | CWE-942 |
| **Clickjacking** | Missing frame protection | CWE-1021 |
| **Open Redirect** | Unvalidated redirects | CWE-601 |

### Medium Severity 🟡

| Check | Description | CWE |
|-------|-------------|-----|
| **CSP** | Missing Content Security Policy | CWE-1021 |
| **Insecure Storage** | Sensitive data in localStorage | CWE-312 |
| **Mixed Content** | HTTP in HTTPS pages | - |

### Low Severity 🟢

| Check | Description | Impact |
|-------|-------------|--------|
| **Mobile UX** | Disabled zoom, touch issues | Accessibility |
| **External Links** | Missing `noopener` on `target="_blank"` | Security |

## Framework Standards

### TypeScript/React ⚛️

✅ **Enforced Standards:**
- PascalCase component names
- Functional components (no classes)
- TypeScript interfaces (no PropTypes)
- Avoid `any` type and `@ts-ignore`
- Security: `rel="noopener noreferrer"` on external links

❌ **Violations Detected:**
```typescript
// BAD: Class component
class MyComponent extends React.Component { }

// BAD: any type
const data: any = fetchData();

// BAD: @ts-ignore
// @ts-ignore
const result = unsafeOperation();

// BAD: Missing noopener
<a href="https://example.com" target="_blank">Link</a>
```

✅ **Correct:**
```typescript
// GOOD: Functional component
const MyComponent: React.FC = () => { }

// GOOD: Specific types
const data: UserData = fetchData();

// GOOD: Fix type issues
const result = safeOperation();

// GOOD: Secure external link
<a href="https://example.com" target="_blank" rel="noopener noreferrer">Link</a>
```

### Python 3 🐍

✅ **Enforced Standards:**
- Type hints on all functions
- Google-style docstrings
- Python 3 syntax (no Python 2)
- Security: Parameterized queries, no `shell=True`

❌ **Violations Detected:**
```python
# BAD: No type hints
def process_data(data):
    return data

# BAD: SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# BAD: Command injection risk
os.system(f"ls {user_input}")
```

✅ **Correct:**
```python
# GOOD: Type hints and docstring
def process_data(data: Dict[str, Any]) -> ProcessedData:
    """
    Process input data and return structured result.

    Args:
        data: Input data dictionary

    Returns:
        ProcessedData object
    """
    return ProcessedData(data)

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# GOOD: Safe subprocess
subprocess.run(["ls", user_input])
```

### HTML/CSS v2 🌐

✅ **Enforced Standards:**
- Pure code (no frameworks)
- Semantic HTML5
- WCAG 2.1 accessibility
- Mobile-first responsive
- CSP headers
- Input sanitization

❌ **Violations Detected:**
```html
<!-- BAD: Missing CSP -->
<head>
  <title>My App</title>
</head>

<!-- BAD: Non-semantic -->
<div class="header">
  <div class="nav">...</div>
</div>

<!-- BAD: Disabled zoom -->
<meta name="viewport" content="user-scalable=no">
```

✅ **Correct:**
```html
<!-- GOOD: CSP included -->
<head>
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; ...">
  <title>My App</title>
</head>

<!-- GOOD: Semantic HTML -->
<header>
  <nav>...</nav>
</header>

<!-- GOOD: Zoom enabled -->
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
```

## Integration Examples

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running security scan..."

python3 security-agent/agent.py --exit-on-critical

if [ $? -ne 0 ]; then
    echo "❌ Critical security issues found!"
    echo "📊 Review: security-agent/reports/"
    exit 1
fi

echo "✅ Security check passed!"
```

### GitHub Actions (Already Configured)

See `.github/workflows/security-scan.yml` for automatic scanning on:
- Every push to main/develop
- All pull requests
- Weekly schedule (Sundays)
- Manual dispatch

### npm Scripts (Already Configured)

```bash
npm run security:scan          # Run scan with all reports
npm run security:report         # Generate HTML report only
npm run security:ci             # CI mode (exit on critical)
```

## Report Examples

### Console Output

```
🔍 Mobile Security & Standards Agent
====================================
Starting scan at 2025-10-31 10:30:00

📁 Scanning 142 files...

====================================
📊 SCAN SUMMARY
====================================

⏱️  Duration: 3.45s
📁 Files scanned: 142

🔒 SECURITY ISSUES:
  🔴 CRITICAL: 3
  🟠 HIGH: 5
  🟡 MEDIUM: 8
  🟢 LOW: 2

📋 STANDARDS VIOLATIONS: 12

⚠️  CRITICAL ISSUES FOUND - IMMEDIATE ACTION REQUIRED!

📄 JSON report: security-agent/reports/security-report-20251031_103000.json
📄 Markdown report: security-agent/reports/security-report-20251031_103000.md
📄 HTML report: security-agent/reports/security-report-20251031_103000.html
```

### HTML Report Preview

The HTML report includes:
- 📊 Interactive dashboard with statistics
- 🎨 Color-coded severity levels
- 📝 Code snippets with syntax highlighting
- 💡 Actionable recommendations
- 🔗 CWE references with links
- 📱 Mobile-responsive design

## Configuration

Customize behavior in `security-agent/config/agent-config.json`:

```json
{
  "security": {
    "mobileAttacks": {
      "enabled": true,
      "checks": [
        "xss",              // Enable/disable specific checks
        "injection",
        "csrf",
        // ... more checks
      ]
    },
    "severity": {
      "critical": ["xss", "injection", "csrf"],
      "high": ["cors", "clickjacking"],
      // ... customize severity levels
    }
  },
  "scanning": {
    "paths": {
      "include": ["src/**/*.ts", "api/**/*.js", "v2/**/*.html"],
      "exclude": ["node_modules/**", "dist/**"]
    }
  }
}
```

## Best Practices

### 1. Run Regularly
- ✅ Before every commit (pre-commit hook)
- ✅ In CI/CD pipeline
- ✅ Weekly full scans

### 2. Prioritize Fixes
1. 🔴 Critical → Fix immediately
2. 🟠 High → Fix within 24-48 hours
3. 🟡 Medium → Fix within sprint
4. 🟢 Low → Backlog/next release

### 3. Review Reports
- Share HTML reports with team
- Discuss patterns in retrospectives
- Track metrics over time

### 4. Educate Team
- Review common violations
- Share security guidelines
- Conduct training sessions

## Comparison: v1 vs v2

| Feature | v1 (React) | v2 (Pure) |
|---------|-----------|-----------|
| Security Score | 85/100 | 95/100 |
| Mobile Score | 80/100 | 95/100 |
| Bundle Size | ~200KB | ~30KB |
| Dependencies | 50+ | 0 |
| Attack Surface | Medium | Minimal |
| CSP Support | Partial | Full |

## Troubleshooting

### Issue: "Permission denied"
```bash
chmod +x security-agent/run-agent.sh
```

### Issue: "Python not found"
```bash
# Install Python 3.8+
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3

# Windows
# Download from python.org
```

### Issue: "No reports generated"
```bash
# Check permissions
ls -la security-agent/reports/

# Create directory
mkdir -p security-agent/reports
```

## Support

- 📖 Full docs: `security-agent/README.md`
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

## License

Same as parent project.
