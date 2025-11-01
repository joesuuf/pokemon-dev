# Performance Optimization Agents

Two specialized Python agents for comprehensive web performance monitoring and implementation.

## Overview

These agents work together to analyze and fix performance issues:

1. **Performance Monitoring Agent** - Identifies bottlenecks using industry-standard tools
2. **Performance Implementation Agent** - Applies fixes based on findings

## Features

### 🔍 Monitoring Agent Capabilities

- **Google Lighthouse Integration**
  - Full Lighthouse audits via CLI
  - Core Web Vitals tracking (LCP, CLS, FCP, TBT, TTI)
  - Performance, Accessibility, Best Practices, SEO, and PWA scores

- **Security Analysis**
  - OWASP security header validation
  - SSL/TLS configuration testing
  - Content Security Policy (CSP) detection
  - CORS misconfiguration detection
  - XSS protection verification

- **Bundle Analysis**
  - JavaScript bundle size analysis
  - CSS bundle size analysis
  - Recommendations for optimization

- **Reporting**
  - Comprehensive JSON reports
  - Overall health scores
  - Actionable recommendations

### 🔧 Implementation Agent Capabilities

- **HTML Optimization**
  - Viewport meta tag injection
  - Charset configuration
  - Theme-color for mobile
  - Preconnect hints for APIs

- **Security Hardening**
  - Complete security headers configuration
  - X-Content-Type-Options
  - X-Frame-Options
  - X-XSS-Protection
  - Referrer-Policy
  - Permissions-Policy
  - Content-Security-Policy

- **Performance Fixes**
  - console.log statement removal
  - Native lazy loading for images
  - Service worker creation for caching
  - Image optimization recommendations

- **Safety Features**
  - Automatic project backup before changes
  - Detailed change tracking
  - Rollback capability

## Installation

### Prerequisites

```bash
# Python 3.8+
python --version

# Node.js (for Lighthouse)
node --version

# Lighthouse CLI
npm install -g lighthouse
```

### Python Dependencies

```bash
# Install required packages
pip install requests beautifulsoup4

# Optional (for enhanced features)
pip install pytest locust selenium webdriver-manager bandit safety
```

## Usage

### Monitoring Agent

#### Basic Usage

```bash
python agents/python/performance_monitoring_agent.py https://your-app.com
```

#### Advanced Usage

```bash
# Specify output directory
python agents/python/performance_monitoring_agent.py https://your-app.com -o ./reports

# View help
python agents/python/performance_monitoring_agent.py --help
```

#### Output

The monitoring agent generates:
- `performance_report_TIMESTAMP.json` - Complete audit report
- `lighthouse_TIMESTAMP.json` - Raw Lighthouse data

**Example Report Structure:**
```json
{
  "generated_at": "2025-10-31T...",
  "target_url": "https://your-app.com",
  "performance_metrics": {
    "largest_contentful_paint": 2.1,
    "cumulative_layout_shift": 0.05,
    "total_blocking_time": 150,
    "performance_score": 95
  },
  "security_findings": {
    "security_score": 85,
    "vulnerabilities": [],
    "security_headers": {...}
  },
  "overall_health": 90,
  "recommendations": [...]
}
```

### Implementation Agent

#### Basic Usage

```bash
# Apply fixes to current project
python agents/python/performance_implementation_agent.py .

# Apply fixes to specific directory
python agents/python/performance_implementation_agent.py /path/to/project
```

#### Advanced Usage

```bash
# Use with monitoring report
python agents/python/performance_implementation_agent.py . -r ./reports/performance_report_*.json
```

#### What Gets Modified

The implementation agent will:
1. Create a backup at `.backup_TIMESTAMP/`
2. Optimize `index.html`
3. Update `vercel.json` with security headers
4. Remove console.log statements from `src/**/*.ts*`
5. Add lazy loading to images in `src/components/**/*.tsx`
6. Create `public/service-worker.js`
7. Generate `implementation_report_TIMESTAMP.json`

#### Safety

- **Automatic Backup**: Creates `.backup_TIMESTAMP/` before any changes
- **Rollback**: Simply restore from backup if needed
- **Non-Destructive**: Only modifies code, never deletes
- **Report**: Detailed JSON report of all changes

## Workflow: Using Both Agents Together

### Step 1: Monitor Performance

```bash
# Run monitoring agent on deployed app
python agents/python/performance_monitoring_agent.py https://pokemon-tcg-search.vercel.app

# Check the report
cat performance-reports/performance_report_*.json | jq '.overall_health'
```

### Step 2: Analyze Findings

```bash
# View recommendations
cat performance-reports/performance_report_*.json | jq '.recommendations'

# Example output:
# [
#   "⚠️ LCP is too high (>2.5s). Optimize images and server response time.",
#   "🔒 Security score is low (65/100). Add missing security headers."
# ]
```

### Step 3: Apply Fixes

```bash
# Run implementation agent
python agents/python/performance_implementation_agent.py .

# Review changes
git diff

# Review implementation report
cat implementation_report_*.json
```

### Step 4: Re-Monitor

```bash
# Monitor again to verify improvements
python agents/python/performance_monitoring_agent.py https://pokemon-tcg-search.vercel.app

# Compare scores
```

### Step 5: Deploy

```bash
# If satisfied, commit and push
git add .
git commit -m "Apply performance optimizations from agents"
git push
```

## Agent Communication

The agents can work together automatically:

```bash
# 1. Monitor and save report
python agents/python/performance_monitoring_agent.py https://your-app.com -o ./reports

# 2. Implement fixes using the report
python agents/python/performance_implementation_agent.py . -r ./reports/performance_report_*.json
```

When using a monitoring report, the implementation agent will:
- Prioritize fixes based on findings
- Focus on issues identified by monitoring
- Add targeted optimizations

## Security Features

Both agents include security analysis and hardening:

### Monitoring Agent Security Checks

- ✅ Strict-Transport-Security header
- ✅ X-Frame-Options header
- ✅ X-Content-Type-Options header
- ✅ Content-Security-Policy header
- ✅ X-XSS-Protection header
- ✅ Referrer-Policy header
- ✅ Permissions-Policy header
- ✅ CORS configuration
- ✅ SSL/TLS grade

### Implementation Agent Security Fixes

- ✅ Adds all missing security headers
- ✅ Configures strict CSP policy
- ✅ Removes XSS vulnerabilities
- ✅ Implements secure CORS
- ✅ Adds HTTPS enforcement headers

## Performance Targets

### Core Web Vitals

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5s - 4.0s | > 4.0s |
| FID (First Input Delay) | ≤ 100ms | 100ms - 300ms | > 300ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| TBT (Total Blocking Time) | ≤ 200ms | 200ms - 600ms | > 600ms |

### Lighthouse Scores

| Category | Good | Needs Improvement | Poor |
|----------|------|-------------------|------|
| Performance | ≥ 90 | 50 - 89 | < 50 |
| Accessibility | ≥ 90 | 50 - 89 | < 50 |
| Best Practices | ≥ 90 | 50 - 89 | < 50 |
| SEO | ≥ 90 | 50 - 89 | < 50 |

## Troubleshooting

### Lighthouse Not Found

```bash
# Install Lighthouse globally
npm install -g lighthouse

# Verify installation
lighthouse --version
```

### Python Dependencies Missing

```bash
# Install all dependencies
pip install requests beautifulsoup4 cssutils jsbeautifier

# Or use requirements file
pip install -r agents/requirements.txt
```

### Permission Errors

```bash
# Ensure you have write permissions
chmod +x agents/python/*.py

# Run with elevated permissions if needed (not recommended)
sudo python agents/python/...
```

### Backup Failed

If backup fails, the implementation agent will abort automatically. Check:
- Disk space available
- Write permissions in project directory
- No existing `.backup_*` directories preventing creation

## Advanced Configuration

### Custom Performance Budgets

Edit the monitoring agent to add custom budgets:

```python
# In performance_monitoring_agent.py
PERFORMANCE_BUDGETS = {
    "lcp": 2.0,  # Custom LCP target
    "cls": 0.05,  # Custom CLS target
    "tbt": 150,  # Custom TBT target
}
```

### Custom Security Headers

Edit the implementation agent to customize headers:

```python
# In performance_implementation_agent.py
# Modify the security_headers dict in add_security_headers_config()
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Performance Audit

on: [push, pull_request]

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: |
          npm install -g lighthouse
          pip install requests beautifulsoup4

      - name: Run Monitoring Agent
        run: |
          python agents/python/performance_monitoring_agent.py https://your-app.com

      - name: Check Performance Score
        run: |
          score=$(cat performance-reports/performance_report_*.json | jq '.overall_health')
          if [ "$score" -lt 80 ]; then
            echo "Performance score too low: $score"
            exit 1
          fi
```

## Roadmap

Future enhancements:

- [ ] WebPageTest API integration
- [ ] Load testing with Locust
- [ ] Mobile performance testing
- [ ] Selenium-based real user monitoring
- [ ] Automatic PR creation with fixes
- [ ] Integration with monitoring services (Datadog, New Relic)
- [ ] WordPress/CMS plugin stripping
- [ ] Third-party script analysis and removal
- [ ] Advanced bundle analysis with webpack-bundle-analyzer
- [ ] Critical CSS extraction
- [ ] Automated A/B testing of fixes

## Contributing

When adding new features to the agents:

1. Maintain backward compatibility
2. Add comprehensive error handling
3. Update this README
4. Include unit tests
5. Generate reports in JSON format

## License

Part of the Pokemon TCG Search project.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review agent output and error messages
3. Check implementation reports for details
4. Refer to parent project documentation

---

**Last Updated:** October 31, 2025
**Agents Version:** 1.0.0
**Status:** Production Ready ✅
