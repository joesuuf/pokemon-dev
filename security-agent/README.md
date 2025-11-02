---
name: Security Agent v2
description: Comprehensive security scanning agent with 10 advanced capabilities - Dynamic testing, dependency analysis, OWASP compliance, automated remediation, performance security, threat modeling, and more
version: 2.0.0
model: claude-sonnet-4
temperature: 0.3
max_tokens: 8192
tools:
  - read
  - write
  - bash
skills_dir: ./skills/security
workflows_dir: ./workflows/security
enabled_skills:
  # Core security scanning
  - scan_xss
  - validate_csrf
  - check_cors
  - validate_csp
  - check_typescript_standards
  - check_python_standards
  - detect_dead_code
  # Enhanced capabilities (v2)
  - dynamic_security_test
  - analyze_dependencies
  - check_compliance
  - generate_remediation
  - performance_security_check
  - check_security_headers
  - analyze_code_quality
  - threat_modeling_stride
  - mobile_advanced_tests
  - setup_monitoring
enabled_workflows:
  - full_security_scan_v2
  - comprehensive_audit
  - owasp_compliance_check
  - dependency_audit
  - performance_security_audit
  - threat_modeling_analysis
categories:
  - Security
  - Standards
  - Code Quality
  - Compliance
  - Threat Modeling
  - Performance
---

# Security Agent v2.0

Comprehensive security scanning agent with advanced capabilities for mobile and web applications.

## Version 2.0 Enhancements

### 🆕 New Capabilities

1. **Dynamic Security Testing** - Runtime pattern detection, URL manipulation analysis
2. **Dependency Vulnerability Analysis** - npm/Python package security scanning
3. **OWASP Top 10 Compliance** - Industry-standard compliance verification
4. **Automated Remediation** - Code examples and auto-fix suggestions
5. **Performance Security** - DoS vulnerability and resource exhaustion detection
6. **HTTP Security Headers** - Comprehensive headers validation
7. **Code Quality Metrics** - Complexity and nesting depth analysis
8. **Advanced Threat Modeling** - STRIDE analysis framework
9. **Mobile Advanced Tests** - ATS, certificate pinning, secure storage
10. **Continuous Monitoring** - CI/CD integration and monitoring setup

## Core Capabilities

### Security Scanning
- **Mobile browser attack detection**: XSS, CSRF, CORS, clickjacking vulnerabilities
- **Injection vulnerability scanning**: SQL injection, command injection, path traversal
- **Dynamic security testing**: Runtime pattern detection, code execution analysis
- **Dependency security**: npm/Python package vulnerability scanning
- **Performance security**: DoS detection, resource exhaustion checks
- **Security headers**: HTTP headers validation and recommendations

### Compliance & Standards
- **OWASP Top 10 compliance**: Full compliance checking and scoring
- **Framework standards**: TypeScript/React, Python 3 standards validation
- **Code quality metrics**: Complexity, nesting depth, function analysis

### Threat Modeling
- **STRIDE analysis**: Comprehensive threat modeling framework
- **Attack surface mapping**: Identification of security boundaries
- **Threat risk assessment**: Prioritized threat identification

### Remediation & Monitoring
- **Automated remediation**: Code examples and fix suggestions
- **Continuous monitoring**: CI/CD integration templates
- **Security training**: Awareness scoring and recommendations

## Workflows

### Full Security Scan v2
Complete security audit including all v2 enhancements:
1. Basic security scanning (XSS, CSRF, CORS, CSP)
2. Dynamic security testing
3. Dependency vulnerability analysis
4. OWASP Top 10 compliance check
5. Performance security analysis
6. Security headers validation
7. Code quality metrics
8. Threat modeling (STRIDE)
9. Mobile advanced tests
10. Generate comprehensive report

### Comprehensive Audit
Complete security audit with remediation suggestions:
1. Execute full security scan
2. Generate remediation suggestions
3. Provide code examples for fixes
4. Create compliance report
5. Generate monitoring configuration

### OWASP Compliance Check
Focus on OWASP Top 10 compliance:
1. Map findings to OWASP categories
2. Calculate compliance scores
3. Generate compliance gap analysis
4. Provide remediation roadmap

### Dependency Audit
Third-party security analysis:
1. Scan package.json and requirements.txt
2. Check for known vulnerabilities
3. Validate version pinning
4. Generate dependency report

### Performance Security Audit
DoS and resource exhaustion detection:
1. Check for infinite loops
2. Analyze unbounded recursion
3. Verify timeout handling
4. Check rate limiting implementation
5. Resource exhaustion analysis

### Threat Modeling Analysis
STRIDE-based threat analysis:
1. Spoofing threat analysis
2. Tampering threat analysis
3. Repudiation threat analysis
4. Information Disclosure analysis
5. Denial of Service analysis
6. Elevation of Privilege analysis

## Configuration

See `security-agent/config/agent-config-v2.json` for full configuration options.

## Usage

```bash
# Run comprehensive security scan
python agents/python/security_agent_v2.py .

# Run with specific workflow
python agents/python/security_agent_v2.py . -w comprehensive_audit

# Generate JSON report
python agents/python/security_agent_v2.py . -o security-report-v2.json

# Use via npm script
npm run security:scan:v2
```

## Output Format

Follows standardized agent output schema with enhanced v2 fields:

```json
{
  "schema_version": "2.0.0",
  "agent": {
    "name": "Security Agent v2",
    "version": "2.0.0",
    "category": "security"
  },
  "execution": {
    "timestamp": "ISO-8601",
    "duration_ms": 0.0,
    "status": "success|error"
  },
  "results": {
    "security_issues": [...],
    "dynamic_security_findings": [...],
    "dependency_vulnerabilities": [...],
    "compliance_scores": {...},
    "performance_security_issues": [...],
    "threat_modeling_results": {...},
    "remediation_suggestions": [...]
  }
}
```

## Integration

- **Modular Framework**: Fully integrated with `modular_agent_framework.py`
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins templates included
- **Monitoring**: Continuous monitoring setup available
- **Reporting**: JSON, HTML, Markdown report formats

## Requirements

- Python 3.12+
- See `security-agent/requirements.txt` for dependencies

## Migration from v1

v1 agents are archived in `security-agent/v1/`. v2 is backward compatible with v1 configuration but adds extensive new capabilities.
