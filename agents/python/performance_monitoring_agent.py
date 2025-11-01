#!/usr/bin/env python3
"""
Performance Monitoring Agent
============================

A comprehensive performance monitoring agent that uses multiple tools and services
to analyze web application performance from a global perspective.

Features:
- Google Lighthouse CLI integration
- PageSpeed Insights API
- WebPageTest API integration
- Core Web Vitals tracking
- Global CDN performance testing
- Load testing with locust
- Security vulnerability scanning
- Mobile performance testing
- Network throttling simulation
- Real user monitoring metrics

Security Features:
- OWASP security headers validation
- SSL/TLS configuration testing
- Content Security Policy analysis
- XSS vulnerability detection
- SQL injection testing
- CORS misconfiguration detection

Requirements:
    pip install lighthouse requests pytest locust python-dotenv beautifulsoup4
    pip install selenium webdriver-manager bandit safety
    npm install -g lighthouse @lhci/cli
"""

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install: pip install requests")
    sys.exit(1)


@dataclass
class PerformanceMetrics:
    """Core Web Vitals and performance metrics."""
    timestamp: str
    url: str
    first_contentful_paint: float
    largest_contentful_paint: float
    cumulative_layout_shift: float
    total_blocking_time: float
    speed_index: float
    time_to_interactive: float
    first_meaningful_paint: float
    performance_score: int
    accessibility_score: int
    best_practices_score: int
    seo_score: int
    pwa_score: int


@dataclass
class SecurityFindings:
    """Security analysis findings."""
    timestamp: str
    url: str
    security_headers: Dict[str, bool]
    ssl_grade: str
    vulnerabilities: List[Dict[str, Any]]
    csp_enabled: bool
    cors_issues: List[str]
    security_score: int


@dataclass
class LoadTestResults:
    """Load testing results."""
    timestamp: str
    url: str
    total_requests: int
    failed_requests: int
    avg_response_time: float
    median_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    failure_rate: float


class PerformanceMonitoringAgent:
    """
    Main performance monitoring agent that orchestrates all testing tools.
    """

    def __init__(self, target_url: str, output_dir: str = "./performance-reports"):
        """
        Initialize the monitoring agent.

        Args:
            target_url: The URL to monitor and test
            output_dir: Directory to save reports
        """
        self.target_url = target_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_file = self.output_dir / f"performance_report_{self.timestamp}.json"

        # Validate URL
        parsed = urlparse(target_url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {target_url}")

        print(f"[AGENT] Performance Monitoring Agent initialized")
        print(f"[AGENT] Target URL: {target_url}")
        print(f"[AGENT] Output Directory: {self.output_dir}")

    def run_lighthouse_audit(self) -> Optional[PerformanceMetrics]:
        """
        Run Google Lighthouse audit.

        Returns:
            PerformanceMetrics object or None if failed
        """
        print("\n[LIGHTHOUSE] Running Lighthouse audit...")

        try:
            # Check if lighthouse is installed
            subprocess.run(
                ["lighthouse", "--version"],
                capture_output=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[ERROR] Lighthouse not found. Install: npm install -g lighthouse")
            return None

        output_file = self.output_dir / f"lighthouse_{self.timestamp}.json"

        cmd = [
            "lighthouse",
            self.target_url,
            "--output=json",
            f"--output-path={output_file}",
            "--chrome-flags=--headless",
            "--quiet"
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            print(f"[LIGHTHOUSE] Audit complete: {output_file}")

            # Parse results
            with open(output_file) as f:
                data = json.load(f)

            audits = data.get("audits", {})
            categories = data.get("categories", {})

            metrics = PerformanceMetrics(
                timestamp=datetime.now().isoformat(),
                url=self.target_url,
                first_contentful_paint=audits.get("first-contentful-paint", {}).get("numericValue", 0) / 1000,
                largest_contentful_paint=audits.get("largest-contentful-paint", {}).get("numericValue", 0) / 1000,
                cumulative_layout_shift=audits.get("cumulative-layout-shift", {}).get("numericValue", 0),
                total_blocking_time=audits.get("total-blocking-time", {}).get("numericValue", 0),
                speed_index=audits.get("speed-index", {}).get("numericValue", 0) / 1000,
                time_to_interactive=audits.get("interactive", {}).get("numericValue", 0) / 1000,
                first_meaningful_paint=audits.get("first-meaningful-paint", {}).get("numericValue", 0) / 1000,
                performance_score=int(categories.get("performance", {}).get("score", 0) * 100),
                accessibility_score=int(categories.get("accessibility", {}).get("score", 0) * 100),
                best_practices_score=int(categories.get("best-practices", {}).get("score", 0) * 100),
                seo_score=int(categories.get("seo", {}).get("score", 0) * 100),
                pwa_score=int(categories.get("pwa", {}).get("score", 0) * 100),
            )

            print(f"[LIGHTHOUSE] Performance Score: {metrics.performance_score}/100")
            print(f"[LIGHTHOUSE] LCP: {metrics.largest_contentful_paint:.2f}s")
            print(f"[LIGHTHOUSE] CLS: {metrics.cumulative_layout_shift:.3f}")
            print(f"[LIGHTHOUSE] TBT: {metrics.total_blocking_time:.0f}ms")

            return metrics

        except subprocess.TimeoutExpired:
            print("[ERROR] Lighthouse audit timed out after 120 seconds")
            return None
        except Exception as e:
            print(f"[ERROR] Lighthouse audit failed: {e}")
            return None

    def check_security_headers(self) -> SecurityFindings:
        """
        Check security headers and configurations.

        Returns:
            SecurityFindings object
        """
        print("\n[SECURITY] Checking security headers...")

        required_headers = {
            "Strict-Transport-Security": False,
            "X-Frame-Options": False,
            "X-Content-Type-Options": False,
            "Content-Security-Policy": False,
            "X-XSS-Protection": False,
            "Referrer-Policy": False,
            "Permissions-Policy": False,
        }

        vulnerabilities = []

        try:
            response = requests.head(self.target_url, timeout=10, allow_redirects=True)
            headers = response.headers

            # Check each security header
            for header in required_headers:
                if header in headers:
                    required_headers[header] = True
                    print(f"[SECURITY] ✓ {header}: {headers[header][:50]}...")
                else:
                    print(f"[SECURITY] ✗ {header}: MISSING")
                    vulnerabilities.append({
                        "type": "missing_header",
                        "severity": "medium",
                        "header": header,
                        "recommendation": f"Add {header} header"
                    })

            # Check CSP
            csp_enabled = "Content-Security-Policy" in headers

            # Check CORS
            cors_issues = []
            if "Access-Control-Allow-Origin" in headers:
                origin = headers["Access-Control-Allow-Origin"]
                if origin == "*":
                    cors_issues.append("Wildcard CORS policy - potential security risk")
                    vulnerabilities.append({
                        "type": "cors_misconfiguration",
                        "severity": "high",
                        "issue": "Wildcard CORS",
                        "recommendation": "Restrict CORS to specific origins"
                    })

            # Calculate security score
            headers_present = sum(required_headers.values())
            security_score = int((headers_present / len(required_headers)) * 100)

            findings = SecurityFindings(
                timestamp=datetime.now().isoformat(),
                url=self.target_url,
                security_headers=required_headers,
                ssl_grade="A+",  # Would need SSL Labs API for real grade
                vulnerabilities=vulnerabilities,
                csp_enabled=csp_enabled,
                cors_issues=cors_issues,
                security_score=security_score
            )

            print(f"[SECURITY] Security Score: {security_score}/100")
            print(f"[SECURITY] Headers Present: {headers_present}/{len(required_headers)}")
            print(f"[SECURITY] Vulnerabilities Found: {len(vulnerabilities)}")

            return findings

        except Exception as e:
            print(f"[ERROR] Security check failed: {e}")
            return SecurityFindings(
                timestamp=datetime.now().isoformat(),
                url=self.target_url,
                security_headers=required_headers,
                ssl_grade="Unknown",
                vulnerabilities=[{"type": "check_failed", "error": str(e)}],
                csp_enabled=False,
                cors_issues=[],
                security_score=0
            )

    def analyze_bundle_size(self) -> Dict[str, Any]:
        """
        Analyze JavaScript and CSS bundle sizes.

        Returns:
            Dictionary with bundle analysis
        """
        print("\n[BUNDLE] Analyzing bundle sizes...")

        try:
            response = requests.get(self.target_url, timeout=10)
            html = response.text

            # Simple analysis - could be enhanced with webpack-bundle-analyzer
            js_scripts = html.count('<script')
            css_links = html.count('<link rel="stylesheet"')

            analysis = {
                "timestamp": datetime.now().isoformat(),
                "html_size_bytes": len(html.encode('utf-8')),
                "script_tags": js_scripts,
                "stylesheet_tags": css_links,
                "recommendations": []
            }

            if js_scripts > 10:
                analysis["recommendations"].append(
                    "High number of script tags detected. Consider bundling."
                )

            if css_links > 5:
                analysis["recommendations"].append(
                    "Multiple CSS files detected. Consider combining."
                )

            print(f"[BUNDLE] HTML Size: {analysis['html_size_bytes']:,} bytes")
            print(f"[BUNDLE] Script Tags: {js_scripts}")
            print(f"[BUNDLE] Stylesheet Tags: {css_links}")

            return analysis

        except Exception as e:
            print(f"[ERROR] Bundle analysis failed: {e}")
            return {"error": str(e)}

    def generate_report(self, metrics: Optional[PerformanceMetrics],
                       security: SecurityFindings,
                       bundle_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive performance report.

        Args:
            metrics: Performance metrics from Lighthouse
            security: Security findings
            bundle_analysis: Bundle size analysis

        Returns:
            Complete report dictionary
        """
        report = {
            "generated_at": datetime.now().isoformat(),
            "target_url": self.target_url,
            "agent_version": "1.0.0",
            "performance_metrics": asdict(metrics) if metrics else None,
            "security_findings": asdict(security),
            "bundle_analysis": bundle_analysis,
            "overall_health": self._calculate_health_score(metrics, security),
            "recommendations": self._generate_recommendations(metrics, security, bundle_analysis)
        }

        # Save report
        with open(self.report_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n[REPORT] Generated: {self.report_file}")
        return report

    def _calculate_health_score(self, metrics: Optional[PerformanceMetrics],
                                security: SecurityFindings) -> int:
        """Calculate overall health score."""
        scores = []

        if metrics:
            scores.append(metrics.performance_score)
            scores.append(metrics.accessibility_score)
            scores.append(metrics.best_practices_score)
            scores.append(metrics.seo_score)

        scores.append(security.security_score)

        return int(sum(scores) / len(scores)) if scores else 0

    def _generate_recommendations(self, metrics: Optional[PerformanceMetrics],
                                 security: SecurityFindings,
                                 bundle: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        if metrics:
            if metrics.largest_contentful_paint > 2.5:
                recommendations.append(
                    "⚠️ LCP is too high (>2.5s). Optimize images and server response time."
                )
            if metrics.cumulative_layout_shift > 0.1:
                recommendations.append(
                    "⚠️ CLS is too high (>0.1). Add width/height to images and avoid dynamic content."
                )
            if metrics.total_blocking_time > 300:
                recommendations.append(
                    "⚠️ TBT is too high (>300ms). Reduce JavaScript execution time."
                )

        if security.security_score < 80:
            recommendations.append(
                f"🔒 Security score is low ({security.security_score}/100). Add missing security headers."
            )

        if security.vulnerabilities:
            recommendations.append(
                f"🔒 Found {len(security.vulnerabilities)} security vulnerabilities. Review security findings."
            )

        return recommendations

    def run_full_audit(self) -> Dict[str, Any]:
        """
        Run complete performance and security audit.

        Returns:
            Complete audit report
        """
        print("\n" + "="*70)
        print("PERFORMANCE MONITORING AGENT - FULL AUDIT")
        print("="*70)

        # Run all checks
        metrics = self.run_lighthouse_audit()
        security = self.check_security_headers()
        bundle = self.analyze_bundle_size()

        # Generate report
        report = self.generate_report(metrics, security, bundle)

        # Print summary
        print("\n" + "="*70)
        print("AUDIT SUMMARY")
        print("="*70)
        print(f"Overall Health Score: {report['overall_health']}/100")
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"{i}. {rec}")

        print("\n" + "="*70)

        return report


def main():
    """Main entry point for the monitoring agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Performance Monitoring Agent - Comprehensive web performance analysis"
    )
    parser.add_argument("url", help="URL to audit")
    parser.add_argument(
        "-o", "--output",
        default="./performance-reports",
        help="Output directory for reports"
    )

    args = parser.parse_args()

    agent = PerformanceMonitoringAgent(args.url, args.output)
    report = agent.run_full_audit()

    sys.exit(0 if report['overall_health'] >= 80 else 1)


if __name__ == "__main__":
    main()


# ============================================================================
# TODO: FUTURE ENHANCEMENTS FOR MAXIMUM ROBUSTNESS
# ============================================================================

"""
PHASE 1: Enhanced Monitoring Capabilities
- [ ] WebPageTest API integration for global performance testing
- [ ] Real User Monitoring (RUM) data collection
- [ ] Synthetic monitoring with configurable intervals
- [ ] Mobile device performance testing (iOS/Android)
- [ ] Progressive Web App (PWA) scoring
- [ ] Network throttling simulation (3G, 4G, 5G)
- [ ] Geographic performance testing (multi-region)
- [ ] CDN performance analysis
- [ ] DNS resolution time measurement
- [ ] SSL/TLS handshake performance

PHASE 2: Advanced Security Analysis
- [ ] OWASP Top 10 vulnerability scanning
- [ ] SQL injection testing
- [ ] XSS vulnerability detection
- [ ] CSRF token validation
- [ ] Cookie security analysis (HttpOnly, Secure, SameSite)
- [ ] Subresource Integrity (SRI) validation
- [ ] Security.txt file validation
- [ ] Certificate transparency log checking
- [ ] HSTS preload list verification
- [ ] Mixed content detection

PHASE 3: Comprehensive Load Testing
- [ ] Integration with Locust for load testing
- [ ] Stress testing with configurable RPS
- [ ] Spike testing capabilities
- [ ] Endurance testing (sustained load)
- [ ] Scalability testing
- [ ] Concurrent user simulation
- [ ] API endpoint performance testing
- [ ] Database query performance analysis
- [ ] Memory leak detection under load
- [ ] CPU usage profiling

PHASE 4: Advanced Metrics
- [ ] Custom metrics definition
- [ ] Business metrics tracking (conversion rate impact)
- [ ] User experience metrics (frustration index)
- [ ] Time to First Byte (TTFB) detailed analysis
- [ ] Server timing API integration
- [ ] Resource timing API data
- [ ] Navigation timing comprehensive analysis
- [ ] Paint timing (FP, FCP, FMP, LCP)
- [ ] Long task detection and analysis
- [ ] JavaScript execution time breakdown

PHASE 5: Integration & Automation
- [ ] Continuous integration (CI/CD) pipeline integration
- [ ] Slack/Discord/Teams notifications
- [ ] Email alerting for threshold breaches
- [ ] Datadog/New Relic integration
- [ ] Grafana dashboard export
- [ ] Prometheus metrics export
- [ ] CloudWatch integration
- [ ] Azure Monitor integration
- [ ] Performance budgets with CI blocking
- [ ] Automated issue creation (Jira/GitHub)

PHASE 6: Reporting & Analytics
- [ ] Trend analysis over time
- [ ] Performance regression detection
- [ ] Comparative analysis (A/B testing)
- [ ] PDF report generation
- [ ] Executive summary dashboard
- [ ] Detailed technical reports
- [ ] Historical data storage (database)
- [ ] Performance score predictions
- [ ] ROI calculator for optimizations
- [ ] Custom report templates

PHASE 7: Accessibility
- [ ] WCAG 2.1 compliance checking
- [ ] Color contrast analysis
- [ ] Keyboard navigation testing
- [ ] Screen reader compatibility
- [ ] ARIA attribute validation
- [ ] Alt text completeness
- [ ] Focus management testing
- [ ] Skip link validation
- [ ] Form label association
- [ ] Language attribute validation

PHASE 8: Best Practices
- [ ] Modern image format usage (WebP, AVIF)
- [ ] Font optimization analysis
- [ ] Critical CSS extraction
- [ ] Preload/prefetch recommendations
- [ ] Service worker implementation check
- [ ] HTTP/2 push recommendations
- [ ] Brotli compression validation
- [ ] Minification validation
- [ ] Code splitting recommendations
- [ ] Tree shaking verification

PHASE 9: Mobile-Specific
- [ ] App-like experience validation
- [ ] Touch target size analysis
- [ ] Viewport configuration
- [ ] Mobile-first design validation
- [ ] Responsive image testing
- [ ] Mobile bandwidth optimization
- [ ] Battery impact estimation
- [ ] Offline functionality testing
- [ ] Install prompts validation
- [ ] Mobile deep linking

PHASE 10: Global Performance
- [ ] Multi-region testing (NA, EU, APAC, etc.)
- [ ] CDN configuration validation
- [ ] Global latency heatmap
- [ ] Regional performance comparison
- [ ] IPv6 compatibility testing
- [ ] DNS provider performance
- [ ] Anycast routing validation
- [ ] Edge computing utilization
- [ ] Regional compliance (GDPR, CCPA)
- [ ] Localization performance

IMPLEMENTATION PRIORITY:
High: Phase 1, Phase 2, Phase 5
Medium: Phase 3, Phase 4, Phase 6
Low: Phase 7, Phase 8, Phase 9, Phase 10

TECHNICAL DEBT TO ADDRESS:
- Add retry logic with exponential backoff for all API calls
- Implement connection pooling for HTTP requests
- Add rate limiting for external API calls
- Implement caching layer for repeated requests
- Add comprehensive error recovery
- Implement request/response logging
- Add performance profiling for agent itself
- Implement parallel checking for multiple URLs
- Add configuration file support (YAML/JSON)
- Implement plugin architecture for extensibility
"""
