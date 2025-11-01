#!/usr/bin/env python3
"""
Security Agent
==============

Modular security scanning agent following Anthropic's best practices.
Integrates existing security-agent functionality into the modular framework.

Features:
- Mobile browser attack detection (XSS, CSRF, CORS, clickjacking)
- Framework standards checking (TypeScript/React, Python)
- Dead code detection
- Security vulnerability scanning
- Standards compliance validation

Requirements:
    pip install jsonschema requests

Based on:
- https://www.anthropic.com/research/building-effective-agents
- https://docs.claude.com/en/docs/claude-code/agent-skills
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

# Import framework base
from modular_agent_framework import ModularAgent, AgentSkill, AgentConfig

# Try to import schema validator (may not exist yet)
try:
    from lib.schema_validator import validate_output
    from lib.agent_communication import create_agent_output
except ImportError:
    validate_output = None
    create_agent_output = None


class Severity(Enum):
    """Severity levels for security issues"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SecurityIssue:
    """Represents a security issue found during scanning"""
    category: str
    severity: Severity
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    recommendation: str
    cwe_id: Optional[str] = None
    mobile_specific: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "category": self.category,
            "severity": self.severity.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "description": self.description,
            "recommendation": self.recommendation,
            "cwe_id": self.cwe_id,
            "mobile_specific": self.mobile_specific
        }


@dataclass
class StandardsViolation:
    """Represents a framework standards violation"""
    framework: str
    rule: str
    file_path: str
    line_number: int
    code_snippet: str
    expected: str
    actual: str
    auto_fixable: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "framework": self.framework,
            "rule": self.rule,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet,
            "expected": self.expected,
            "actual": self.actual,
            "auto_fixable": self.auto_fixable
        }


@dataclass
class UnusedFile:
    """Represents a potentially unused or outdated file"""
    file_path: str
    reason: str
    confidence: str  # high, medium, low
    last_modified: str
    file_size: int
    references_found: int
    suggested_action: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "file_path": self.file_path,
            "reason": self.reason,
            "confidence": self.confidence,
            "last_modified": self.last_modified,
            "file_size": self.file_size,
            "references_found": self.references_found,
            "suggested_action": self.suggested_action
        }


class MobileSecurityScanner:
    """Scanner for mobile browser security vulnerabilities"""

    # XSS patterns
    XSS_PATTERNS = [
        (r'dangerouslySetInnerHTML\s*=', "Dangerous HTML injection point", "CWE-79"),
        (r'innerHTML\s*=', "Direct innerHTML assignment can lead to XSS", "CWE-79"),
        (r'outerHTML\s*=', "Direct outerHTML assignment can lead to XSS", "CWE-79"),
        (r'document\.write\s*\(', "document.write can lead to XSS", "CWE-79"),
        (r'eval\s*\(', "eval() can execute malicious code", "CWE-95"),
        (r'new\s+Function\s*\(', "Function constructor can execute malicious code", "CWE-95"),
        (r'setTimeout\s*\(\s*["\']', "setTimeout with string argument can lead to code injection", "CWE-95"),
        (r'setInterval\s*\(\s*["\']', "setInterval with string argument can lead to code injection", "CWE-95"),
    ]

    # Storage patterns
    INSECURE_STORAGE_PATTERNS = [
        (r'localStorage\.setItem\s*\([^,]*(?:password|token|secret|key|auth)',
         "Sensitive data in localStorage (accessible via XSS)", "CWE-312"),
        (r'sessionStorage\.setItem\s*\([^,]*(?:password|token|secret|key|auth)',
         "Sensitive data in sessionStorage (accessible via XSS)", "CWE-312"),
    ]

    # API Key exposure patterns
    API_KEY_PATTERNS = [
        (r'(?:api[_-]?key|apikey|api[_-]?secret)\s*[:=]\s*["\'][^"\']+["\']',
         "Hardcoded API key detected", "CWE-798"),
        (r'(?:password|passwd|pwd)\s*[:=]\s*["\'][^"\']+["\']',
         "Hardcoded password detected", "CWE-798"),
        (r'(?:secret|token)\s*[:=]\s*["\'][^"\']+["\']',
         "Hardcoded secret/token detected", "CWE-798"),
    ]

    # CORS patterns
    CORS_PATTERNS = [
        (r'Access-Control-Allow-Origin\s*:\s*\*',
         "Overly permissive CORS policy", "CWE-942"),
        (r'cors\s*\(\s*\{\s*origin\s*:\s*["\']?\*',
         "Wildcard CORS origin", "CWE-942"),
    ]

    # Mobile-specific patterns
    MOBILE_PATTERNS = [
        (r'viewport\s*=.*user-scalable\s*=\s*no',
         "Disabling zoom can harm accessibility on mobile", None),
        (r'touch(?:start|move|end)\s*=.*preventDefault',
         "Preventing touch default may break mobile UX", None),
        (r'window\.open\s*\([^)]*(?:_blank)(?!.*noopener)',
         "Missing noopener on external links (mobile tabnabbing)", "CWE-1022"),
    ]

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.security_config = config.get("security", {})
        self.enabled_checks = set(self.security_config.get("mobileAttacks", {}).get("checks", []))
        self.severity_map = self.security_config.get("severity", {})

    def scan_file(self, file_path: Path) -> List[SecurityIssue]:
        """Scan a single file for security issues"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, start=1):
                # XSS checks
                if "xss" in self.enabled_checks or "injection" in self.enabled_checks:
                    issues.extend(self._check_patterns(
                        line, line_num, file_path, self.XSS_PATTERNS, "xss"
                    ))

                # Insecure storage checks
                if "insecureStorage" in self.enabled_checks:
                    issues.extend(self._check_patterns(
                        line, line_num, file_path, self.INSECURE_STORAGE_PATTERNS,
                        "insecureStorage"
                    ))

                # API key exposure
                if "sensitiveDataExposure" in self.enabled_checks:
                    issues.extend(self._check_patterns(
                        line, line_num, file_path, self.API_KEY_PATTERNS,
                        "sensitiveDataExposure"
                    ))

                # CORS issues
                if "cors" in self.enabled_checks:
                    issues.extend(self._check_patterns(
                        line, line_num, file_path, self.CORS_PATTERNS, "cors"
                    ))

                # Mobile-specific issues
                if "mobileSpecific" in self.enabled_checks:
                    mobile_issues = self._check_patterns(
                        line, line_num, file_path, self.MOBILE_PATTERNS, "mobileSpecific"
                    )
                    for issue in mobile_issues:
                        issue.mobile_specific = True
                    issues.extend(mobile_issues)

            # File-level checks
            content = ''.join(lines)
            issues.extend(self._check_csp(content, file_path))
            issues.extend(self._check_csrf_protection(content, file_path))

        except Exception as e:
            print(f"Error scanning {file_path}: {e}", file=sys.stderr)

        return issues

    def _check_patterns(self, line: str, line_num: int, file_path: Path,
                       patterns: List[Tuple[str, str, Optional[str]]],
                       category: str) -> List[SecurityIssue]:
        """Check line against a list of regex patterns"""
        issues = []

        for pattern, description, cwe_id in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                severity = self._get_severity(category)
                recommendation = self._get_recommendation(category, pattern)

                issues.append(SecurityIssue(
                    category=category,
                    severity=severity,
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    description=description,
                    recommendation=recommendation,
                    cwe_id=cwe_id
                ))

        return issues

    def _check_csp(self, content: str, file_path: Path) -> List[SecurityIssue]:
        """Check for Content Security Policy"""
        issues = []

        if "csp" not in self.enabled_checks:
            return issues

        # Check HTML files for CSP meta tags
        if file_path.suffix in ['.html', '.htm']:
            if 'Content-Security-Policy' not in content:
                issues.append(SecurityIssue(
                    category="csp",
                    severity=Severity.MEDIUM,
                    file_path=str(file_path),
                    line_number=1,
                    code_snippet="<head> section",
                    description="Missing Content Security Policy",
                    recommendation="Add CSP meta tag or header to prevent XSS attacks",
                    cwe_id="CWE-1021"
                ))

        return issues

    def _check_csrf_protection(self, content: str, file_path: Path) -> List[SecurityIssue]:
        """Check for CSRF protection in forms"""
        issues = []

        if "csrf" not in self.enabled_checks:
            return issues

        # Check for forms without CSRF tokens
        if file_path.suffix in ['.tsx', '.jsx', '.html']:
            form_matches = re.finditer(r'<form[^>]*method\s*=\s*["\']post["\']', content, re.IGNORECASE)
            for match in form_matches:
                # Check if there's a CSRF token nearby
                surrounding = content[max(0, match.start()-100):min(len(content), match.end()+500)]
                if not re.search(r'csrf|_token|authenticity', surrounding, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    issues.append(SecurityIssue(
                        category="csrf",
                        severity=Severity.CRITICAL,
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=match.group(0),
                        description="POST form without CSRF protection",
                        recommendation="Add CSRF token to form submissions",
                        cwe_id="CWE-352"
                    ))

        return issues

    def _get_severity(self, category: str) -> Severity:
        """Get severity level for a category"""
        if not self.severity_map:
            # Default severity mapping
            severity_map = {
                "critical": ["csrf", "sensitiveDataExposure"],
                "high": ["cors"],
                "medium": ["csp", "insecureStorage"],
                "low": ["mobileSpecific"]
            }
        else:
            severity_map = self.severity_map

        for severity_name, categories in severity_map.items():
            if category in categories:
                return Severity(severity_name)
        return Severity.INFO

    def _get_recommendation(self, category: str, pattern: str) -> str:
        """Get security recommendation based on category"""
        recommendations = {
            "xss": "Sanitize user input and use safe DOM manipulation methods. Consider using DOMPurify or similar libraries.",
            "insecureStorage": "Use secure storage mechanisms. For sensitive data, use server-side sessions or encrypted storage.",
            "sensitiveDataExposure": "Never hardcode credentials. Use environment variables and secure secret management.",
            "cors": "Restrict CORS to specific trusted origins. Avoid using wildcard (*).",
            "csp": "Implement Content Security Policy to restrict resource loading and prevent XSS.",
            "csrf": "Implement CSRF tokens for state-changing operations.",
            "mobileSpecific": "Follow mobile web best practices for accessibility and user experience."
        }
        return recommendations.get(category, "Review and fix security issue.")


class TypeScriptReactStandardsChecker:
    """Checker for TypeScript/React framework standards"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ts_config = config.get("frameworks", {}).get("typescript", {})
        self.react_config = self.ts_config.get("standards", {}).get("react", {})

    def check_file(self, file_path: Path) -> List[StandardsViolation]:
        """Check a TypeScript/React file for standards violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                content = ''.join(lines)

            # Check component naming
            violations.extend(self._check_component_naming(file_path, content))

            # Check for class components (should use functional)
            if self.react_config.get("functionalComponents"):
                violations.extend(self._check_class_components(file_path, lines))

            # Check for PropTypes (should use TypeScript)
            if not self.react_config.get("propTypes"):
                violations.extend(self._check_proptypes(file_path, lines))

            # Check TypeScript strict mode compliance
            violations.extend(self._check_typescript_types(file_path, lines))

            # Check security patterns
            violations.extend(self._check_react_security(file_path, lines))

        except Exception as e:
            print(f"Error checking {file_path}: {e}", file=sys.stderr)

        return violations

    def _check_component_naming(self, file_path: Path, content: str) -> List[StandardsViolation]:
        """Check component file and function naming conventions"""
        violations = []

        # Component files should be PascalCase
        filename = file_path.stem
        if file_path.suffix in ['.tsx', '.jsx']:
            if filename[0].islower() and filename != 'index':
                violations.append(StandardsViolation(
                    framework="TypeScript/React",
                    rule="Component files must use PascalCase naming",
                    file_path=str(file_path),
                    line_number=1,
                    code_snippet=f"File: {file_path.name}",
                    expected="PascalCase (e.g., MyComponent.tsx)",
                    actual=f"{filename} (camelCase or snake_case)",
                    auto_fixable=True
                ))

        return violations

    def _check_class_components(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for class components (should use functional components)"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            if re.search(r'class\s+\w+\s+extends\s+(?:React\.)?Component', line):
                violations.append(StandardsViolation(
                    framework="TypeScript/React",
                    rule="Use functional components instead of class components",
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    expected="Functional component with hooks",
                    actual="Class component",
                    auto_fixable=False
                ))

        return violations

    def _check_proptypes(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for PropTypes usage (should use TypeScript interfaces)"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            if 'PropTypes' in line and 'import' not in line:
                violations.append(StandardsViolation(
                    framework="TypeScript/React",
                    rule="Use TypeScript interfaces instead of PropTypes",
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    expected="TypeScript interface or type",
                    actual="PropTypes",
                    auto_fixable=False
                ))

        return violations

    def _check_typescript_types(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for TypeScript type safety violations"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            # Check for 'any' type
            if re.search(r':\s*any\b', line) and '//' not in line[:line.find('any')]:
                violations.append(StandardsViolation(
                    framework="TypeScript",
                    rule="Avoid using 'any' type - use specific types",
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    expected="Specific type definition",
                    actual="any type",
                    auto_fixable=False
                ))

            # Check for @ts-ignore
            if '@ts-ignore' in line:
                violations.append(StandardsViolation(
                    framework="TypeScript",
                    rule="Avoid @ts-ignore - fix type issues instead",
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    expected="Proper type definition",
                    actual="@ts-ignore comment",
                    auto_fixable=False
                ))

        return violations

    def _check_react_security(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check React security best practices"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            # Check for target="_blank" without noopener
            if re.search(r'target\s*=\s*["\']_blank["\']', line):
                if 'noopener' not in line and 'noreferrer' not in line:
                    violations.append(StandardsViolation(
                        framework="React Security",
                        rule="External links with target='_blank' must include rel='noopener noreferrer'",
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        expected="rel=\"noopener noreferrer\"",
                        actual="Missing noopener/noreferrer",
                        auto_fixable=True
                    ))

        return violations


class PythonStandardsChecker:
    """Checker for Python 3 framework standards"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.py_config = config.get("frameworks", {}).get("python", {})
        self.security_config = self.py_config.get("standards", {}).get("security", {})

    def check_file(self, file_path: Path) -> List[StandardsViolation]:
        """Check a Python file for standards violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Check Python version compatibility
            violations.extend(self._check_python_version(file_path, lines))

            # Check for type hints
            if self.py_config.get("standards", {}).get("typeHints"):
                violations.extend(self._check_type_hints(file_path, lines))

            # Check for docstrings
            violations.extend(self._check_docstrings(file_path, lines))

            # Check security issues
            violations.extend(self._check_security(file_path, lines))

        except Exception as e:
            print(f"Error checking {file_path}: {e}", file=sys.stderr)

        return violations

    def _check_python_version(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for Python 2 syntax or deprecated features"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            # Check for print statements (Python 2)
            if re.search(r'^\s*print\s+[^(]', line):
                violations.append(StandardsViolation(
                    framework="Python 3",
                    rule="Use print() function, not print statement",
                    file_path=str(file_path),
                    line_number=line_num,
                    code_snippet=line.strip(),
                    expected="print()",
                    actual="print statement",
                    auto_fixable=True
                ))

        return violations

    def _check_type_hints(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for missing type hints"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            # Check function definitions without type hints
            if re.search(r'^\s*def\s+\w+\s*\([^)]*\)\s*:', line):
                if '->' not in line and '__init__' not in line:
                    violations.append(StandardsViolation(
                        framework="Python 3",
                        rule="Functions should include type hints",
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        expected="def func(param: Type) -> ReturnType:",
                        actual="Missing type hints",
                        auto_fixable=False
                    ))

        return violations

    def _check_docstrings(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for missing docstrings"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            if re.search(r'^\s*def\s+\w+\s*\(', line):
                # Check if next non-empty line is a docstring
                if line_num < len(lines):
                    next_line = lines[line_num].strip() if line_num < len(lines) else ""
                    if not next_line.startswith('"""') and not next_line.startswith("'''"):
                        violations.append(StandardsViolation(
                            framework="Python 3",
                            rule="Functions should have docstrings",
                            file_path=str(file_path),
                            line_number=line_num,
                            code_snippet=line.strip(),
                            expected="Google-style docstring",
                            actual="Missing docstring",
                            auto_fixable=False
                        ))

        return violations

    def _check_security(self, file_path: Path, lines: List[str]) -> List[StandardsViolation]:
        """Check for security issues in Python code"""
        violations = []

        for line_num, line in enumerate(lines, start=1):
            # SQL injection
            if self.security_config.get("sqlInjection"):
                if re.search(r'execute\s*\([^)]*%\s*["\']', line):
                    violations.append(StandardsViolation(
                        framework="Python Security",
                        rule="Potential SQL injection - use parameterized queries",
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        expected="execute('SELECT * FROM table WHERE id = ?', (id,))",
                        actual="String formatting in SQL query",
                        auto_fixable=False
                    ))

            # Command injection
            if self.security_config.get("commandInjection"):
                if re.search(r'os\.system\s*\(|subprocess\..*shell\s*=\s*True', line):
                    violations.append(StandardsViolation(
                        framework="Python Security",
                        rule="Potential command injection - avoid shell=True",
                        file_path=str(file_path),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        expected="subprocess.run([cmd, arg1, arg2])",
                        actual="shell=True or os.system()",
                        auto_fixable=False
                    ))

        return violations


class DeadCodeDetector:
    """Detector for unused and outdated code files"""

    def __init__(self, config: Dict[str, Any], root_dir: Path):
        self.config = config
        self.root_dir = root_dir
        self.dead_code_config = config.get("deadCode", {})
        self.all_files: List[Path] = []
        self.file_references: Dict[str, int] = {}

    def detect_unused_files(self, scanned_files: List[Path]) -> List[UnusedFile]:
        """Detect potentially unused files in the codebase"""
        if not self.dead_code_config.get("enabled", False):
            return []

        self.all_files = scanned_files
        unused_files = []

        # Build reference map
        self._build_reference_map()

        # Check each file
        for file_path in scanned_files:
            unused_file = self._analyze_file(file_path)
            if unused_file:
                unused_files.append(unused_file)

        return unused_files

    def _build_reference_map(self):
        """Build a map of how many times each file is referenced"""
        for file_path in self.all_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Look for imports and references in the content
                for other_file in self.all_files:
                    if other_file == file_path:
                        continue

                    # Get filename patterns to search for
                    filename = other_file.stem
                    relative_path = str(other_file.relative_to(self.root_dir))

                    # Count references
                    count = 0

                    # TypeScript/JavaScript imports
                    patterns = [
                        rf'import.*["\'].*{re.escape(filename)}["\']',
                        rf'require\(["\'].*{re.escape(filename)}["\']',
                        rf'from.*["\'].*{re.escape(filename)}["\']',
                    ]

                    for pattern in patterns:
                        count += len(re.findall(pattern, content, re.IGNORECASE))

                    # Also check for direct file path references
                    if relative_path in content or filename in content:
                        count += 1

                    if count > 0:
                        ref_path = str(other_file)
                        self.file_references[ref_path] = self.file_references.get(ref_path, 0) + count

            except Exception as e:
                continue

    def _analyze_file(self, file_path: Path) -> Optional[UnusedFile]:
        """Analyze a single file to determine if it's unused"""
        try:
            stats = file_path.stat()
            last_modified = datetime.fromtimestamp(stats.st_mtime).isoformat()
            file_size = stats.st_size

            file_path_str = str(file_path)
            references = self.file_references.get(file_path_str, 0)

            # Criteria for unused file detection
            reasons = []
            confidence = "low"

            # Check 1: No references found
            if references == 0:
                reasons.append("No imports or references found in codebase")
                confidence = "high"

            # Check 2: Old file patterns (deprecated naming conventions)
            filename = file_path.name
            if any(pattern in filename for pattern in ['old', 'backup', 'deprecated', 'temp', 'test2', 'copy']):
                reasons.append(f"Filename suggests deprecated/backup code: '{filename}'")
                if confidence == "high":
                    confidence = "high"
                else:
                    confidence = "medium"

            # Check 3: Already prefixed with underscore
            if filename.startswith('_') and not filename.startswith('__'):
                reasons.append("File already marked with underscore prefix (staged for removal)")
                confidence = "high"

            # Check 4: Empty or nearly empty files
            if file_size < 100:  # Less than 100 bytes
                reasons.append(f"Nearly empty file ({file_size} bytes)")
                if confidence != "high":
                    confidence = "medium"

            # Check 5: Old file extensions or patterns
            if file_path.suffix in ['.old', '.bak', '.backup', '.tmp']:
                reasons.append(f"Backup/temporary file extension: {file_path.suffix}")
                confidence = "high"

            # Only report if we found reasons
            if reasons:
                suggested_action = self._get_suggested_action(confidence, references)

                return UnusedFile(
                    file_path=str(file_path.relative_to(self.root_dir)),
                    reason="; ".join(reasons),
                    confidence=confidence,
                    last_modified=last_modified,
                    file_size=file_size,
                    references_found=references,
                    suggested_action=suggested_action
                )

        except Exception as e:
            pass

        return None

    def _get_suggested_action(self, confidence: str, references: int) -> str:
        """Get suggested action based on confidence level"""
        if confidence == "high" and references == 0:
            return "Rename with underscore prefix to verify, then delete if no issues arise"
        elif confidence == "high":
            return f"Review {references} reference(s), then consider removal"
        elif confidence == "medium":
            return "Review file usage and consider marking for removal"
        else:
            return "Manual review recommended"


class SecurityAgent(ModularAgent):
    """
    Security monitoring agent that scans code for vulnerabilities
    and standards violations.
    """

    def __init__(self, config):
        """Initialize security agent"""
        # Load default config if path is provided
        if isinstance(config, (str, Path)):
            config_path = Path(config)
            if not config_path.exists():
                # Try to load from security-agent config
                default_config_path = Path(__file__).parent.parent.parent / "security-agent" / "config" / "agent-config.json"
                if default_config_path.exists():
                    with open(default_config_path) as f:
                        self.agent_config = json.load(f)
                else:
                    self.agent_config = self._get_default_config()
            else:
                super().__init__(config)
                return
        
        # If config is AgentConfig, initialize normally
        super().__init__(config)
        
        # Load agent config for security checks
        default_config_path = Path(__file__).parent.parent.parent / "security-agent" / "config" / "agent-config.json"
        if default_config_path.exists():
            with open(default_config_path) as f:
                self.agent_config = json.load(f)
        else:
            self.agent_config = self._get_default_config()

        self.root_dir = Path.cwd()
        self.security_scanner = MobileSecurityScanner(self.agent_config)
        self.ts_checker = TypeScriptReactStandardsChecker(self.agent_config)
        self.py_checker = PythonStandardsChecker(self.agent_config)
        self.dead_code_detector = DeadCodeDetector(self.agent_config, self.root_dir)

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "security": {
                "mobileAttacks": {
                    "enabled": True,
                    "checks": ["xss", "injection", "csrf", "cors", "csp", "sensitiveDataExposure", "mobileSpecific"]
                },
                "severity": {
                    "critical": ["csrf", "sensitiveDataExposure"],
                    "high": ["cors"],
                    "medium": ["csp", "insecureStorage"],
                    "low": ["mobileSpecific"]
                }
            },
            "frameworks": {
                "typescript": {
                    "enabled": True,
                    "standards": {
                        "react": {
                            "functionalComponents": True,
                            "propTypes": False
                        }
                    }
                },
                "python": {
                    "enabled": True,
                    "standards": {
                        "typeHints": False,
                        "security": {
                            "sqlInjection": True,
                            "commandInjection": True
                        }
                    }
                }
            },
            "deadCode": {
                "enabled": True
            }
        }

    def _register_core_skills(self):
        """Register core security scanning skills"""
        
        # Skill 1: XSS Scanner
        def scan_xss(context: Dict[str, Any]) -> Dict[str, Any]:
            """Scan for XSS vulnerabilities"""
            target_path = Path(context.get('target_path', '.'))
            issues = []
            
            # Get files to scan
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                if file_path.suffix in ['.ts', '.tsx', '.js', '.jsx', '.html']:
                    file_issues = self.security_scanner.scan_file(file_path)
                    issues.extend([issue.to_dict() for issue in file_issues])
            
            return {
                'security_issues': [issue for issue in issues if issue['category'] == 'xss'],
                'issues_count': len([i for i in issues if i['category'] == 'xss'])
            }
        
        self.register_skill(AgentSkill(
            name='scan_xss',
            description='Scan for XSS vulnerabilities',
            category='security',
            function=scan_xss,
            required_tools=['read'],
            config={'severity_threshold': 'high'}
        ))
        
        # Skill 2: CSRF Validator
        def validate_csrf(context: Dict[str, Any]) -> Dict[str, Any]:
            """Validate CSRF protection"""
            target_path = Path(context.get('target_path', '.'))
            issues = []
            
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                if file_path.suffix in ['.tsx', '.jsx', '.html']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        file_issues = self.security_scanner._check_csrf_protection(content, file_path)
                        issues.extend([issue.to_dict() for issue in file_issues])
                    except Exception as e:
                        pass
            
            return {
                'csrf_validated': len(issues) == 0,
                'csrf_issues': issues,
                'issues_count': len(issues)
            }
        
        self.register_skill(AgentSkill(
            name='validate_csrf',
            description='Validate CSRF protection',
            category='security',
            function=validate_csrf,
            required_tools=['read']
        ))
        
        # Skill 3: CORS Checker
        def check_cors(context: Dict[str, Any]) -> Dict[str, Any]:
            """Check CORS configuration"""
            target_path = Path(context.get('target_path', '.'))
            issues = []
            
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                file_issues = self.security_scanner.scan_file(file_path)
                cors_issues = [issue.to_dict() for issue in file_issues if issue.category == 'cors']
                issues.extend(cors_issues)
            
            return {
                'cors_issues': issues,
                'issues_count': len(issues)
            }
        
        self.register_skill(AgentSkill(
            name='check_cors',
            description='Check CORS configuration',
            category='security',
            function=check_cors,
            required_tools=['read']
        ))
        
        # Skill 4: CSP Validator
        def validate_csp(context: Dict[str, Any]) -> Dict[str, Any]:
            """Validate Content Security Policy"""
            target_path = Path(context.get('target_path', '.'))
            issues = []
            
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                if file_path.suffix in ['.html', '.htm']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        file_issues = self.security_scanner._check_csp(content, file_path)
                        issues.extend([issue.to_dict() for issue in file_issues])
                    except Exception as e:
                        pass
            
            return {
                'csp_validated': len(issues) == 0,
                'csp_issues': issues,
                'issues_count': len(issues)
            }
        
        self.register_skill(AgentSkill(
            name='validate_csp',
            description='Validate Content Security Policy',
            category='security',
            function=validate_csp,
            required_tools=['read']
        ))
        
        # Skill 5: TypeScript/React Standards Checker
        def check_typescript_standards(context: Dict[str, Any]) -> Dict[str, Any]:
            """Check TypeScript/React standards"""
            target_path = Path(context.get('target_path', '.'))
            violations = []
            
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                if file_path.suffix in ['.ts', '.tsx', '.jsx']:
                    file_violations = self.ts_checker.check_file(file_path)
                    violations.extend([v.to_dict() for v in file_violations])
            
            return {
                'standards_violations': violations,
                'violations_count': len(violations)
            }
        
        self.register_skill(AgentSkill(
            name='check_typescript_standards',
            description='Check TypeScript/React framework standards',
            category='standards',
            function=check_typescript_standards,
            required_tools=['read']
        ))
        
        # Skill 6: Python Standards Checker
        def check_python_standards(context: Dict[str, Any]) -> Dict[str, Any]:
            """Check Python standards"""
            target_path = Path(context.get('target_path', '.'))
            violations = []
            
            files_to_scan = self._get_files_to_scan(target_path)
            
            for file_path in files_to_scan:
                if file_path.suffix == '.py':
                    file_violations = self.py_checker.check_file(file_path)
                    violations.extend([v.to_dict() for v in file_violations])
            
            return {
                'standards_violations': violations,
                'violations_count': len(violations)
            }
        
        self.register_skill(AgentSkill(
            name='check_python_standards',
            description='Check Python framework standards',
            category='standards',
            function=check_python_standards,
            required_tools=['read']
        ))
        
        # Skill 7: Dead Code Detector
        def detect_dead_code(context: Dict[str, Any]) -> Dict[str, Any]:
            """Detect unused or dead code files"""
            target_path = Path(context.get('target_path', '.'))
            
            files_to_scan = self._get_files_to_scan(target_path)
            unused_files = self.dead_code_detector.detect_unused_files(files_to_scan)
            
            return {
                'unused_files': [f.to_dict() for f in unused_files],
                'unused_files_count': len(unused_files)
            }
        
        self.register_skill(AgentSkill(
            name='detect_dead_code',
            description='Detect unused and outdated code files',
            category='maintenance',
            function=detect_dead_code,
            required_tools=['read']
        ))

    def _get_files_to_scan(self, target_path: Path) -> List[Path]:
        """Get list of files to scan based on configuration"""
        include_patterns = self.agent_config.get("scanning", {}).get("paths", {}).get("include", [
            "src/**/*.ts",
            "src/**/*.tsx",
            "src/**/*.js",
            "src/**/*.jsx",
            "**/*.py"
        ])
        exclude_patterns = self.agent_config.get("scanning", {}).get("paths", {}).get("exclude", [
            "node_modules/**",
            "dist/**",
            "build/**",
            "coverage/**",
            ".git/**"
        ])

        files = []

        for pattern in include_patterns:
            for file_path in target_path.glob(pattern):
                if file_path.is_file():
                    # Check if file should be excluded
                    excluded = False
                    for exclude_pattern in exclude_patterns:
                        if file_path.match(exclude_pattern):
                            excluded = True
                            break

                    if not excluded:
                        files.append(file_path)

        return sorted(set(files))

    def run(self, target_path: str = ".", **kwargs) -> Dict[str, Any]:
        """Run security scan"""
        start_time = datetime.now()
        context = {'target_path': target_path}
        
        # Execute workflow if specified
        if 'workflow' in kwargs and kwargs['workflow'] in self.workflows:
            results = self.execute_workflow(kwargs['workflow'], context)
        else:
            # Run all security skills
            results = {
                'security_issues': [],
                'standards_violations': [],
                'unused_files': []
            }
            
            for skill_name in self.skills:
                try:
                    result = self.execute_skill(skill_name, context=context)
                    
                    # Aggregate results
                    if 'security_issues' in result:
                        results['security_issues'].extend(result['security_issues'])
                    if 'standards_violations' in result:
                        results['standards_violations'].extend(result['standards_violations'])
                    if 'unused_files' in result:
                        results['unused_files'].extend(result['unused_files'])
                    
                    results.update(result)
                except Exception as e:
                    print(f"Error executing skill {skill_name}: {e}", file=sys.stderr)
        
        # Create standardized output
        duration = (datetime.now() - start_time).total_seconds() * 1000
        
        if create_agent_output:
            output = create_agent_output(
                agent_name="Security Agent",
                agent_version="1.0.0",
                category="security",
                results=results,
                execution_time_ms=duration
            )
        else:
            output = {
                "schema_version": "1.0.0",
                "agent": {
                    "name": "Security Agent",
                    "version": "1.0.0",
                    "category": "security"
                },
                "execution": {
                    "timestamp": datetime.now().isoformat(),
                    "duration_ms": duration,
                    "status": "success"
                },
                "results": results
            }
        
        # Validate output if validator is available
        if validate_output:
            is_valid, errors = validate_output(output, "agent-output-schema.json")
            if not is_valid:
                print(f"Warning: Output validation errors: {errors}", file=sys.stderr)
        
        return output


def main():
    """Main entry point"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Security Agent - Modular security scanning")
    parser.add_argument('target_path', nargs='?', default='.', help='Target path to scan')
    parser.add_argument('-w', '--workflow', help='Workflow to execute')
    parser.add_argument('-o', '--output', help='Output file for JSON report')
    parser.add_argument('--config', help='Path to agent config MD file')
    
    args = parser.parse_args()
    
    # Load config
    if args.config:
        config_path = Path(args.config)
    else:
        config_path = Path(__file__).parent.parent / "md" / "security_agent.md"
    
    if not config_path.exists():
        # Create default config
        from modular_agent_framework import AgentConfig
        config = AgentConfig(
            name="Security Agent",
            description="Security scanning and standards validation agent",
            version="1.0.0",
            tools=["read", "write"],
            enabled_skills=["scan_xss", "validate_csrf", "check_cors", "validate_csp",
                          "check_typescript_standards", "check_python_standards", "detect_dead_code"]
        )
        agent = SecurityAgent(config)
    else:
        agent = SecurityAgent(config_path)
    
    # Run scan
    results = agent.run(args.target_path, workflow=args.workflow)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Report saved to {args.output}")
    else:
        print(json.dumps(results, indent=2))
    
    # Exit with error code if critical issues found
    security_issues = results.get('results', {}).get('security_issues', [])
    critical_issues = [issue for issue in security_issues if issue.get('severity') == 'critical']
    
    if critical_issues:
        print(f"\n⚠️  Found {len(critical_issues)} critical security issues!", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()

