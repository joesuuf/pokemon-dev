# Mobile Security & Standards Agent

## Overview

The **Mobile Security & Standards Agent** is an expert system for detecting mobile browser attack vectors and ensuring framework standardization across TypeScript/React, Python 3, and pure HTML/CSS codebases.

## Features

### 🔒 Security Scanning

#### Mobile Browser Attack Detection
- **XSS (Cross-Site Scripting)**: Detects dangerous HTML injection points
  - `dangerouslySetInnerHTML`, `innerHTML`, `outerHTML`
  - `document.write`, `eval`, `Function` constructor
  - String-based `setTimeout`/`setInterval`

- **Injection Attacks**: Code and script injection vulnerabilities
  - SQL injection patterns
  - Command injection
  - Path traversal

- **CSRF Protection**: Verifies CSRF tokens in forms
- **Clickjacking**: Checks for X-Frame-Options and frame-ancestors
- **Open Redirect**: Validates redirect URLs
- **Insecure Storage**: Detects sensitive data in localStorage/sessionStorage
- **Weak Cryptography**: Identifies weak crypto implementations
- **Mixed Content**: HTTP resources in HTTPS pages
- **CSP (Content Security Policy)**: Missing or weak CSP headers
- **CORS Misconfigurations**: Overly permissive CORS policies
- **Sensitive Data Exposure**: Hardcoded API keys, passwords, tokens
- **Mobile-Specific Issues**:
  - Disabled zoom (accessibility issue)
  - `target="_blank"` without `noopener`
  - Touch event mishandling

### 📋 Framework Standards Checking

#### TypeScript/React Standards
- **Component Naming**: PascalCase for components and files
- **Functional Components**: Prefer functional over class components
- **TypeScript Types**: Avoid `any` type and `@ts-ignore`
- **PropTypes**: Use TypeScript interfaces instead of PropTypes
- **Security**: External links with `rel="noopener noreferrer"`
- **Hooks**: Proper React hooks usage

#### Python 3 Standards
- **Version Compatibility**: Python 3 syntax enforcement
- **Type Hints**: Function type annotations
- **Docstrings**: Google-style documentation
- **PEP 8**: Code style compliance
- **Security**:
  - SQL injection prevention
  - Command injection prevention
  - Path traversal protection

#### HTML/CSS Standards (v2)
- **Pure Code**: No frameworks allowed
- **Semantic HTML**: Proper HTML5 semantics
- **Accessibility**: WCAG 2.1 compliance
- **Responsive**: Mobile-first design
- **Security**: CSP headers, input validation

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16+ (for running TypeScript/React project)

### Setup

```bash
# No installation needed! Agent is standalone Python script
cd security-agent

# Make executable (Unix/Linux/Mac)
chmod +x run-agent.sh

# Or use Python directly
python3 agent.py
```

## Usage

### Quick Start

```bash
# From project root
./security-agent/run-agent.sh

# Or from security-agent directory
python3 agent.py

# With custom config
python3 agent.py --config custom-config.json
```

### Command Line Options

```bash
python3 agent.py [OPTIONS]

Options:
  --config PATH         Path to configuration file (default: config/agent-config.json)
  --output-dir PATH     Output directory for reports (default: reports/)
  --format FORMAT       Report format: json, html, markdown, all (default: all)
  --exit-on-critical    Exit with error code if critical issues found
  --parallel            Enable parallel file scanning (default: true)
  --help                Show help message
```

### Integration with npm

Add to your `package.json`:

```json
{
  "scripts": {
    "security:scan": "python3 security-agent/agent.py",
    "security:report": "python3 security-agent/agent.py --format html",
    "security:ci": "python3 security-agent/agent.py --exit-on-critical"
  }
}
```

Then run:

```bash
npm run security:scan
npm run security:report
npm run security:ci  # For CI/CD pipelines
```

### Integration with Git Hooks

#### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "Running Mobile Security & Standards Agent..."

python3 security-agent/agent.py --exit-on-critical

if [ $? -ne 0 ]; then
    echo "❌ Security scan failed! Fix critical issues before committing."
    exit 1
fi

echo "✅ Security scan passed!"
exit 0
```

Make executable:
```bash
chmod +x .git/hooks/pre-commit
```

#### Pre-push Hook

Create `.git/hooks/pre-push`:

```bash
#!/bin/bash

echo "Running comprehensive security scan..."

python3 security-agent/agent.py --format all

echo "📊 Review security reports in security-agent/reports/"
```

## Configuration

The agent is configured via `config/agent-config.json`:

```json
{
  "agent": {
    "name": "Mobile Security & Standards Agent",
    "version": "1.0.0",
    "enabled": true
  },
  "security": {
    "mobileAttacks": {
      "enabled": true,
      "checks": [
        "xss",
        "injection",
        "csrf",
        "clickjacking",
        "openRedirect",
        "insecureStorage",
        "weakCrypto",
        "mixedContent",
        "csp",
        "cors",
        "sensitiveDataExposure",
        "mobileSpecific"
      ]
    },
    "severity": {
      "critical": ["xss", "injection", "csrf", "sensitiveDataExposure"],
      "high": ["clickjacking", "openRedirect", "weakCrypto", "cors"],
      "medium": ["insecureStorage", "mixedContent", "csp"],
      "low": ["mobileSpecific"]
    }
  },
  "frameworks": {
    "typescript": { ... },
    "python": { ... },
    "htmlCss": { ... }
  }
}
```

### Customizing Checks

Enable/disable specific checks:

```json
{
  "security": {
    "mobileAttacks": {
      "checks": [
        "xss",          // Enable XSS detection
        "csrf",         // Enable CSRF detection
        "cors"          // Enable CORS checking
        // Omit others to disable
      ]
    }
  }
}
```

### Custom Severity Levels

```json
{
  "security": {
    "severity": {
      "critical": ["xss", "injection"],
      "high": ["csrf"],
      "medium": ["cors"],
      "low": []
    }
  }
}
```

## Reports

The agent generates three types of reports:

### 1. JSON Report
Machine-readable format for CI/CD integration

```json
{
  "timestamp": "2025-10-31T10:30:00",
  "summary": {
    "files_scanned": 45,
    "security_issues": 12,
    "standards_violations": 8,
    "issues_by_severity": {
      "critical": 2,
      "high": 3,
      "medium": 5,
      "low": 2
    }
  },
  "security_issues": [...],
  "standards_violations": [...]
}
```

### 2. HTML Report
Visual, interactive report for review

Features:
- Color-coded severity levels
- Filterable issues
- Code snippets
- Recommendations
- Issue statistics

### 3. Markdown Report
Human-readable format for documentation

Perfect for:
- Pull request comments
- Security documentation
- Issue tracking
- Team reviews

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/security-scan.yml`:

```yaml
name: Security Scan

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Run Security Agent
      run: |
        python3 security-agent/agent.py --exit-on-critical

    - name: Upload Security Reports
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: security-reports
        path: security-agent/reports/
```

### GitLab CI

Add to `.gitlab-ci.yml`:

```yaml
security_scan:
  stage: test
  image: python:3.10
  script:
    - python3 security-agent/agent.py --exit-on-critical
  artifacts:
    paths:
      - security-agent/reports/
    when: always
  allow_failure: false
```

### Jenkins

```groovy
stage('Security Scan') {
    steps {
        sh 'python3 security-agent/agent.py --exit-on-critical'
    }
    post {
        always {
            archiveArtifacts artifacts: 'security-agent/reports/**/*', allowEmptyArchive: true
        }
    }
}
```

## Understanding Results

### Severity Levels

- 🔴 **CRITICAL**: Immediate security risk, must fix before deployment
  - XSS vulnerabilities
  - SQL/Code injection
  - CSRF missing
  - Hardcoded credentials

- 🟠 **HIGH**: Serious security concern, fix ASAP
  - Weak CORS policies
  - Clickjacking risks
  - Open redirects
  - Weak cryptography

- 🟡 **MEDIUM**: Security improvement recommended
  - Missing CSP
  - Insecure storage
  - Mixed content

- 🟢 **LOW**: Best practice violation
  - Mobile UX issues
  - Accessibility concerns

### Common Issues and Fixes

#### Issue: XSS via dangerouslySetInnerHTML
```typescript
// ❌ BAD
<div dangerouslySetInnerHTML={{__html: userInput}} />

// ✅ GOOD
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{__html: DOMPurify.sanitize(userInput)}} />

// ✅ BETTER - Avoid if possible
<div>{userInput}</div>
```

#### Issue: Hardcoded API Key
```typescript
// ❌ BAD
const API_KEY = "sk_live_abc123def456";

// ✅ GOOD
const API_KEY = import.meta.env.VITE_API_KEY;
```

#### Issue: Missing CSRF Token
```tsx
// ❌ BAD
<form method="post" action="/api/update">
  <input name="data" />
</form>

// ✅ GOOD
<form method="post" action="/api/update">
  <input type="hidden" name="csrf_token" value={csrfToken} />
  <input name="data" />
</form>
```

#### Issue: Insecure External Link
```tsx
// ❌ BAD
<a href="https://example.com" target="_blank">Link</a>

// ✅ GOOD
<a href="https://example.com" target="_blank" rel="noopener noreferrer">Link</a>
```

## Best Practices

### 1. Regular Scans
- Run before every commit (pre-commit hook)
- Run in CI/CD pipeline
- Weekly comprehensive scans

### 2. Fix Critical Issues First
- Prioritize by severity
- Address critical before high
- Document medium/low for backlog

### 3. Review Reports
- Share HTML reports with team
- Discuss patterns and trends
- Update standards as needed

### 4. Educate Team
- Share security findings
- Provide training on common issues
- Create coding guidelines

### 5. Continuous Improvement
- Update agent configuration
- Add custom rules
- Track metrics over time

## Troubleshooting

### Agent Not Finding Files
```bash
# Check scan paths in config
cat security-agent/config/agent-config.json | grep -A 10 "paths"

# Verify files exist
ls -la src/
```

### Permission Denied
```bash
# Make script executable
chmod +x security-agent/run-agent.sh

# Or run directly
python3 security-agent/agent.py
```

### False Positives
```json
// Add exceptions in config
{
  "security": {
    "exceptions": {
      "files": ["src/test/*.test.ts"],
      "patterns": ["// @security-ignore"]
    }
  }
}
```

## Advanced Usage

### Custom Rules

Create `security-agent/custom-rules.py`:

```python
from agent import SecurityIssue, Severity

class CustomSecurityScanner:
    def check_custom_rule(self, file_path, line, line_num):
        if 'MY_DANGEROUS_PATTERN' in line:
            return SecurityIssue(
                category='custom',
                severity=Severity.CRITICAL,
                file_path=str(file_path),
                line_number=line_num,
                code_snippet=line.strip(),
                description='Custom security rule violated',
                recommendation='Fix this custom issue',
                cwe_id='CWE-XXX'
            )
```

## Support

For issues, questions, or feature requests:
1. Check existing issues on GitHub
2. Create new issue with "security-agent" label
3. Include:
   - Agent version
   - Configuration used
   - Sample report
   - Expected vs actual behavior

## Roadmap

- [ ] VS Code extension
- [ ] Real-time scanning (watch mode)
- [ ] Auto-fix capabilities for simple issues
- [ ] Integration with SonarQube
- [ ] SARIF output format
- [ ] Custom rule DSL
- [ ] Machine learning for pattern detection
- [ ] Performance profiling integration

## License

Same as parent project.

## Credits

Built with ❤️ for secure mobile web applications.
