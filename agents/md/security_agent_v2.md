---
name: Security Agent v2
description: Comprehensive security scanning agent with 10 advanced capabilities
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
  - scan_xss
  - validate_csrf
  - check_cors
  - validate_csp
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
  - comprehensive_audit
  - full_security_scan_v2
  - owasp_compliance_check
  - dependency_audit
  - performance_security_audit
  - threat_modeling_analysis
categories:
  - Security
  - Compliance
  - Threat Modeling
  - Performance
---

# Security Agent v2.0

Comprehensive security scanning agent with 10 advanced capabilities integrated into the modular framework.

See `security-agent/README.md` for full documentation.
