#!/usr/bin/env python3
"""
Mobile Security & Standards Agent
Expert agent for mobile browser attack detection and framework standardization
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


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


@dataclass
class ScanResult:
    """Results from a complete security and standards scan"""
    timestamp: str
    security_issues: List[SecurityIssue] = field(default_factory=list)
    standards_violations: List[StandardsViolation] = field(default_factory=list)
    unused_files: List[UnusedFile] = field(default_factory=list)
    files_scanned: int = 0
    scan_duration: float = 0.0

    def get_issue_count_by_severity(self) -> Dict[str, int]:
        """Count issues by severity"""
        counts = {sev.value: 0 for sev in Severity}
        for issue in self.security_issues:
            counts[issue.severity.value] += 1
        return counts

    def has_critical_issues(self) -> bool:
        """Check if there are any critical issues"""
        return any(issue.severity == Severity.CRITICAL for issue in self.security_issues)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "timestamp": self.timestamp,
            "summary": {
                "files_scanned": self.files_scanned,
                "scan_duration": f"{self.scan_duration:.2f}s",
                "security_issues": len(self.security_issues),
                "standards_violations": len(self.standards_violations),
                "unused_files": len(self.unused_files),
                "issues_by_severity": self.get_issue_count_by_severity()
            },
            "security_issues": [issue.to_dict() for issue in self.security_issues],
            "standards_violations": [violation.to_dict() for violation in self.standards_violations],
            "unused_files": [file.to_dict() for file in self.unused_files]
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
                    recommendation="Add CSP meta tag or header to prevent XSS attacks:\n"
                                 "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';\">",
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
        for severity_name, categories in self.severity_map.items():
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

        print("\n🔍 Detecting unused and outdated code...")

        self.all_files = scanned_files
        unused_files = []

        # Build reference map
        self._build_reference_map()

        # Check each file
        for file_path in scanned_files:
            unused_file = self._analyze_file(file_path)
            if unused_file:
                unused_files.append(unused_file)

        print(f"📋 Found {len(unused_files)} potentially unused files")

        return unused_files

    def _build_reference_map(self):
        """Build a map of how many times each file is referenced"""
        print("   Building reference map...")

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

            # Check 4: Duplicate files (similar names)
            similar_files = self._find_similar_files(file_path)
            if similar_files:
                reasons.append(f"Similar files exist: {', '.join([f.name for f in similar_files[:3]])}")
                if confidence != "high":
                    confidence = "medium"

            # Check 5: Empty or nearly empty files
            if file_size < 100:  # Less than 100 bytes
                reasons.append(f"Nearly empty file ({file_size} bytes)")
                if confidence != "high":
                    confidence = "medium"

            # Check 6: Old file extensions or patterns
            if file_path.suffix in ['.old', '.bak', '.backup', '.tmp']:
                reasons.append(f"Backup/temporary file extension: {file_path.suffix}")
                confidence = "high"

            # Check 7: Svelte files when project is React-based
            if file_path.suffix == '.svelte' and self._is_react_project():
                reasons.append("Svelte component in React project (legacy code)")
                confidence = "medium"

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

    def _find_similar_files(self, file_path: Path) -> List[Path]:
        """Find files with similar names"""
        similar = []
        base_name = file_path.stem.lower()

        # Remove common suffixes to find base
        for suffix in ['-old', '_old', '-copy', '_copy', '2', '-backup', '_backup']:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]

        for other_file in self.all_files:
            if other_file == file_path:
                continue

            other_base = other_file.stem.lower()
            if base_name in other_base or other_base in base_name:
                if file_path.suffix == other_file.suffix:
                    similar.append(other_file)

        return similar

    def _is_react_project(self) -> bool:
        """Check if this is a React project"""
        package_json = self.root_dir / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                    return 'react' in deps
            except:
                pass
        return False

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

    def rename_file_with_underscore(self, file_path: Path) -> bool:
        """Rename a file by adding underscore prefix"""
        try:
            new_name = f"_{file_path.name}"
            new_path = file_path.parent / new_name

            if new_path.exists():
                print(f"   ⚠️  Cannot rename {file_path.name}: Target already exists")
                return False

            file_path.rename(new_path)
            print(f"   ✓ Renamed: {file_path.name} → {new_name}")
            return True

        except Exception as e:
            print(f"   ❌ Error renaming {file_path}: {e}")
            return False


class SecurityStandardsAgent:
    """Main agent orchestrating security scans and standards checks"""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the agent with configuration"""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "agent-config.json"

        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.root_dir = Path.cwd()
        self.security_scanner = MobileSecurityScanner(self.config)
        self.ts_checker = TypeScriptReactStandardsChecker(self.config)
        self.py_checker = PythonStandardsChecker(self.config)
        self.dead_code_detector = DeadCodeDetector(self.config, self.root_dir)

        self.scan_result = ScanResult(timestamp=datetime.now().isoformat())

    def scan(self) -> ScanResult:
        """Run complete security and standards scan"""
        start_time = datetime.now()

        print("🔍 Mobile Security & Standards Agent")
        print("=" * 60)
        print(f"Starting scan at {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Get files to scan
        files_to_scan = self._get_files_to_scan()
        self.scan_result.files_scanned = len(files_to_scan)

        print(f"📁 Scanning {len(files_to_scan)} files...\n")

        # Scan each file
        for file_path in files_to_scan:
            self._scan_file(file_path)

        # Detect unused/dead code
        unused_files = self.dead_code_detector.detect_unused_files(files_to_scan)
        self.scan_result.unused_files = unused_files

        # Calculate duration
        end_time = datetime.now()
        self.scan_result.scan_duration = (end_time - start_time).total_seconds()

        # Print summary
        self._print_summary()

        # Generate reports
        self._generate_reports()

        return self.scan_result

    def _get_files_to_scan(self) -> List[Path]:
        """Get list of files to scan based on configuration"""
        include_patterns = self.config.get("scanning", {}).get("paths", {}).get("include", [])
        exclude_patterns = self.config.get("scanning", {}).get("paths", {}).get("exclude", [])

        files = []

        for pattern in include_patterns:
            for file_path in self.root_dir.glob(pattern):
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

    def _scan_file(self, file_path: Path):
        """Scan a single file for security issues and standards violations"""
        try:
            # Security scan
            security_issues = self.security_scanner.scan_file(file_path)
            self.scan_result.security_issues.extend(security_issues)

            # Standards checks
            if file_path.suffix in ['.ts', '.tsx', '.jsx']:
                violations = self.ts_checker.check_file(file_path)
                self.scan_result.standards_violations.extend(violations)

            elif file_path.suffix == '.py':
                violations = self.py_checker.check_file(file_path)
                self.scan_result.standards_violations.extend(violations)

        except Exception as e:
            print(f"❌ Error scanning {file_path}: {e}", file=sys.stderr)

    def _print_summary(self):
        """Print scan summary to console"""
        print("\n" + "=" * 60)
        print("📊 SCAN SUMMARY")
        print("=" * 60)

        print(f"\n⏱️  Duration: {self.scan_result.scan_duration:.2f}s")
        print(f"📁 Files scanned: {self.scan_result.files_scanned}")

        # Security issues by severity
        print("\n🔒 SECURITY ISSUES:")
        issue_counts = self.scan_result.get_issue_count_by_severity()
        for severity, count in issue_counts.items():
            if count > 0:
                icon = self._get_severity_icon(severity)
                print(f"  {icon} {severity.upper()}: {count}")

        print(f"\n📋 STANDARDS VIOLATIONS: {len(self.scan_result.standards_violations)}")

        # Unused files
        if self.scan_result.unused_files:
            print(f"\n🗑️  UNUSED/OUTDATED FILES: {len(self.scan_result.unused_files)}")
            high_conf = sum(1 for f in self.scan_result.unused_files if f.confidence == "high")
            if high_conf > 0:
                print(f"  ⚠️  {high_conf} file(s) with high confidence for removal")

        # Critical issues warning
        if self.scan_result.has_critical_issues():
            print("\n⚠️  CRITICAL ISSUES FOUND - IMMEDIATE ACTION REQUIRED!")

    def _get_severity_icon(self, severity: str) -> str:
        """Get icon for severity level"""
        icons = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
            "info": "ℹ️"
        }
        return icons.get(severity, "•")

    def _generate_reports(self):
        """Generate scan reports in configured formats"""
        report_dir = Path(self.config.get("reporting", {}).get("outputDir", "security-agent/reports"))
        report_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON report
        if "json" in self.config.get("security", {}).get("reportFormat", []):
            json_path = report_dir / f"security-report-{timestamp}.json"
            with open(json_path, 'w') as f:
                json.dump(self.scan_result.to_dict(), f, indent=2)
            print(f"\n📄 JSON report: {json_path}")

        # Markdown report
        if "markdown" in self.config.get("security", {}).get("reportFormat", []):
            md_path = report_dir / f"security-report-{timestamp}.md"
            self._generate_markdown_report(md_path)
            print(f"📄 Markdown report: {md_path}")

        # HTML report
        if "html" in self.config.get("security", {}).get("reportFormat", []):
            html_path = report_dir / f"security-report-{timestamp}.html"
            self._generate_html_report(html_path)
            print(f"📄 HTML report: {html_path}")

        # Unused files report (always generate if found)
        if self.scan_result.unused_files:
            unused_path = report_dir / f"unused-files-{timestamp}.md"
            self._generate_unused_files_report(unused_path)
            print(f"📄 Unused files report: {unused_path}")

    def _generate_markdown_report(self, output_path: Path):
        """Generate markdown report"""
        with open(output_path, 'w') as f:
            f.write("# Mobile Security & Standards Report\n\n")
            f.write(f"**Generated:** {self.scan_result.timestamp}\n\n")
            f.write(f"**Files Scanned:** {self.scan_result.files_scanned}\n\n")
            f.write(f"**Scan Duration:** {self.scan_result.scan_duration:.2f}s\n\n")

            # Security issues
            f.write("## 🔒 Security Issues\n\n")
            issue_counts = self.scan_result.get_issue_count_by_severity()
            for severity, count in issue_counts.items():
                if count > 0:
                    f.write(f"- **{severity.upper()}:** {count}\n")

            f.write("\n### Details\n\n")
            for issue in sorted(self.scan_result.security_issues,
                              key=lambda x: (x.severity.value, x.file_path)):
                f.write(f"#### {issue.severity.value.upper()}: {issue.description}\n\n")
                f.write(f"- **File:** `{issue.file_path}:{issue.line_number}`\n")
                f.write(f"- **Category:** {issue.category}\n")
                if issue.cwe_id:
                    f.write(f"- **CWE:** {issue.cwe_id}\n")
                f.write(f"- **Code:** `{issue.code_snippet}`\n")
                f.write(f"- **Recommendation:** {issue.recommendation}\n\n")

            # Standards violations
            f.write("\n## 📋 Standards Violations\n\n")
            f.write(f"**Total:** {len(self.scan_result.standards_violations)}\n\n")

            for violation in self.scan_result.standards_violations:
                f.write(f"### {violation.framework}: {violation.rule}\n\n")
                f.write(f"- **File:** `{violation.file_path}:{violation.line_number}`\n")
                f.write(f"- **Expected:** {violation.expected}\n")
                f.write(f"- **Actual:** {violation.actual}\n")
                f.write(f"- **Code:** `{violation.code_snippet}`\n")
                f.write(f"- **Auto-fixable:** {'Yes' if violation.auto_fixable else 'No'}\n\n")

    def _generate_html_report(self, output_path: Path):
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Security & Standards Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #2c3e50; margin-bottom: 20px; }}
        h2 {{ color: #34495e; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        h3 {{ color: #555; margin-top: 20px; margin-bottom: 10px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin-bottom: 30px; }}
        .summary-item {{ display: inline-block; margin-right: 30px; }}
        .severity {{ padding: 5px 10px; border-radius: 3px; color: white; font-weight: bold; }}
        .critical {{ background: #e74c3c; }}
        .high {{ background: #e67e22; }}
        .medium {{ background: #f39c12; }}
        .low {{ background: #27ae60; }}
        .info {{ background: #3498db; }}
        .issue, .violation {{
            background: #fff;
            border-left: 4px solid #3498db;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 3px;
        }}
        .issue.critical {{ border-left-color: #e74c3c; }}
        .issue.high {{ border-left-color: #e67e22; }}
        .issue.medium {{ border-left-color: #f39c12; }}
        .issue.low {{ border-left-color: #27ae60; }}
        .code {{ background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 3px; font-family: 'Courier New', monospace; overflow-x: auto; margin: 10px 0; }}
        .meta {{ color: #7f8c8d; font-size: 0.9em; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 Mobile Security & Standards Report</h1>

        <div class="summary">
            <div class="summary-item"><strong>Generated:</strong> {self.scan_result.timestamp}</div>
            <div class="summary-item"><strong>Files Scanned:</strong> {self.scan_result.files_scanned}</div>
            <div class="summary-item"><strong>Duration:</strong> {self.scan_result.scan_duration:.2f}s</div>
        </div>

        <h2>Security Issues Summary</h2>
        <table>
            <tr>
                <th>Severity</th>
                <th>Count</th>
            </tr>
"""

        issue_counts = self.scan_result.get_issue_count_by_severity()
        for severity, count in issue_counts.items():
            if count > 0:
                html += f"""
            <tr>
                <td><span class="severity {severity}">{severity.upper()}</span></td>
                <td>{count}</td>
            </tr>
"""

        html += """
        </table>

        <h2>Security Issues Details</h2>
"""

        for issue in sorted(self.scan_result.security_issues,
                          key=lambda x: (x.severity.value, x.file_path)):
            html += f"""
        <div class="issue {issue.severity.value}">
            <h3>{issue.description}</h3>
            <div class="meta">
                <strong>Severity:</strong> <span class="severity {issue.severity.value}">{issue.severity.value.upper()}</span> |
                <strong>Category:</strong> {issue.category} |
                <strong>File:</strong> {issue.file_path}:{issue.line_number}
                {f' | <strong>CWE:</strong> {issue.cwe_id}' if issue.cwe_id else ''}
            </div>
            <div class="code">{issue.code_snippet}</div>
            <p><strong>Recommendation:</strong> {issue.recommendation}</p>
        </div>
"""

        html += """
        <h2>Standards Violations</h2>
"""

        for violation in self.scan_result.standards_violations:
            html += f"""
        <div class="violation">
            <h3>{violation.framework}: {violation.rule}</h3>
            <div class="meta">
                <strong>File:</strong> {violation.file_path}:{violation.line_number} |
                <strong>Auto-fixable:</strong> {'Yes' if violation.auto_fixable else 'No'}
            </div>
            <div class="code">{violation.code_snippet}</div>
            <p><strong>Expected:</strong> {violation.expected}</p>
            <p><strong>Actual:</strong> {violation.actual}</p>
        </div>
"""

        html += """
    </div>
</body>
</html>
"""

        with open(output_path, 'w') as f:
            f.write(html)

    def _generate_unused_files_report(self, output_path: Path):
        """Generate markdown report for unused/outdated files"""
        with open(output_path, 'w') as f:
            f.write("# Unused & Outdated Files Report\n\n")
            f.write(f"**Generated:** {self.scan_result.timestamp}\n\n")
            f.write(f"**Total Files Found:** {len(self.scan_result.unused_files)}\n\n")

            f.write("---\n\n")

            f.write("## Summary\n\n")
            f.write("This report identifies files that may be unused or outdated in your codebase. ")
            f.write("Files are categorized by confidence level based on various heuristics.\n\n")

            # Count by confidence
            high_conf = [f for f in self.scan_result.unused_files if f.confidence == "high"]
            medium_conf = [f for f in self.scan_result.unused_files if f.confidence == "medium"]
            low_conf = [f for f in self.scan_result.unused_files if f.confidence == "low"]

            f.write(f"- **High Confidence:** {len(high_conf)} files\n")
            f.write(f"- **Medium Confidence:** {len(medium_conf)} files\n")
            f.write(f"- **Low Confidence:** {len(low_conf)} files\n\n")

            f.write("## Recommendation Process\n\n")
            f.write("1. **Review** the files listed below\n")
            f.write("2. **Rename** suspicious files with underscore prefix using the agent\n")
            f.write("3. **Test** your application thoroughly\n")
            f.write("4. **Delete** files if no issues arise\n\n")

            f.write("### Renaming Files\n\n")
            f.write("To rename files with underscore prefix for testing:\n\n")
            f.write("```bash\n")
            f.write("# This renames the file to verify it's not being used\n")
            f.write("# If your app still works, the file is safe to delete\n")
            f.write("python3 security-agent/agent.py --rename-unused\n")
            f.write("```\n\n")

            f.write("---\n\n")

            # High confidence files
            if high_conf:
                f.write("## 🔴 High Confidence (Likely Unused)\n\n")
                f.write("These files are highly likely to be unused based on multiple indicators.\n\n")

                for unused_file in sorted(high_conf, key=lambda x: x.file_path):
                    self._write_unused_file_entry(f, unused_file)

            # Medium confidence files
            if medium_conf:
                f.write("\n## 🟡 Medium Confidence (Review Recommended)\n\n")
                f.write("These files show some signs of being unused but require manual review.\n\n")

                for unused_file in sorted(medium_conf, key=lambda x: x.file_path):
                    self._write_unused_file_entry(f, unused_file)

            # Low confidence files
            if low_conf:
                f.write("\n## 🟢 Low Confidence (Manual Review)\n\n")
                f.write("These files may be unused but need careful review.\n\n")

                for unused_file in sorted(low_conf, key=lambda x: x.file_path):
                    self._write_unused_file_entry(f, unused_file)

            # Footer with commands
            f.write("\n---\n\n")
            f.write("## Actions\n\n")
            f.write("### Rename Files for Testing\n\n")
            f.write("To mark files as potentially unused by adding underscore prefix:\n\n")
            f.write("```bash\n")
            f.write("# Review the list above and add filenames to rename\n")
            f.write("# Example: This would rename LoadingSpinner.svelte to _LoadingSpinner.svelte\n")
            f.write("mv src/components/LoadingSpinner.svelte src/components/_LoadingSpinner.svelte\n")
            f.write("```\n\n")
            f.write("### Test Your Application\n\n")
            f.write("After renaming:\n")
            f.write("1. Run your development server\n")
            f.write("2. Test all major features\n")
            f.write("3. Check for any import errors in console\n")
            f.write("4. Run your test suite\n\n")
            f.write("### Delete Confirmed Unused Files\n\n")
            f.write("If everything works after renaming:\n\n")
            f.write("```bash\n")
            f.write("# Delete the file\n")
            f.write("git rm src/components/_LoadingSpinner.svelte\n")
            f.write("git commit -m \"Remove unused file: LoadingSpinner.svelte\"\n")
            f.write("```\n\n")

            f.write("---\n\n")
            f.write("*Generated by Mobile Security & Standards Agent*\n")

    def _write_unused_file_entry(self, f, unused_file: UnusedFile):
        """Write a single unused file entry to the markdown report"""
        f.write(f"### `{unused_file.file_path}`\n\n")
        f.write(f"**Confidence:** {unused_file.confidence.upper()}\n\n")
        f.write(f"**Reason:** {unused_file.reason}\n\n")
        f.write(f"**Details:**\n")
        f.write(f"- References found: {unused_file.references_found}\n")
        f.write(f"- File size: {unused_file.file_size} bytes\n")
        f.write(f"- Last modified: {unused_file.last_modified}\n\n")
        f.write(f"**Suggested Action:** {unused_file.suggested_action}\n\n")
        f.write("---\n\n")


def main():
    """Main entry point"""
    agent = SecurityStandardsAgent()
    result = agent.scan()

    # Exit with error code if critical issues found and configured
    if result.has_critical_issues() and agent.config.get("reporting", {}).get("exitOnCritical"):
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
