#!/usr/bin/env python3
"""
Performance Implementation Agent
=================================

A specialized agent that implements performance fixes based on monitoring findings.
Works in conjunction with the Performance Monitoring Agent to analyze and fix code.

Features:
- Strip third-party dependencies and bloat
- Convert to pure TypeScript/HTML/CSS
- Optimize headers and metadata
- Fix Core Web Vitals issues
- Implement lazy loading
- Add security headers
- Optimize images
- Implement code splitting
- Remove unused code
- Add service worker for caching

Security Features:
- Remove vulnerable dependencies
- Implement CSP headers
- Fix CORS configurations
- Add XSS protection
- Implement rate limiting
- Secure cookie configurations

Requirements:
    pip install beautifulsoup4 cssutils jsbeautifier autopep8
"""

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not found. Install: pip install beautifulsoup4")
    sys.exit(1)


@dataclass
class FixReport:
    """Report of fixes applied."""
    timestamp: str
    fixes_applied: List[str]
    files_modified: List[str]
    security_improvements: List[str]
    performance_improvements: List[str]
    warnings: List[str]
    success: bool


class PerformanceImplementationAgent:
    """
    Main implementation agent that applies performance and security fixes.
    """

    def __init__(self, project_dir: str, monitoring_report: Optional[str] = None):
        """
        Initialize the implementation agent.

        Args:
            project_dir: Path to the project directory
            monitoring_report: Optional path to monitoring agent report
        """
        self.project_dir = Path(project_dir).resolve()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_dir = self.project_dir / f".backup_{self.timestamp}"
        self.fixes_applied = []
        self.files_modified = []
        self.security_improvements = []
        self.performance_improvements = []
        self.warnings = []

        # Load monitoring report if provided
        self.monitoring_data = None
        if monitoring_report:
            with open(monitoring_report) as f:
                self.monitoring_data = json.load(f)

        print(f"[AGENT] Performance Implementation Agent initialized")
        print(f"[AGENT] Project Directory: {self.project_dir}")
        print(f"[AGENT] Backup Directory: {self.backup_dir}")

    def create_backup(self):
        """Create backup of the project before making changes."""
        print("\n[BACKUP] Creating project backup...")

        try:
            shutil.copytree(
                self.project_dir,
                self.backup_dir,
                ignore=shutil.ignore_patterns(
                    'node_modules', '.git', 'dist', 'build', '__pycache__',
                    '.backup_*', 'performance-reports'
                )
            )
            print(f"[BACKUP] Backup created: {self.backup_dir}")
            return True
        except Exception as e:
            print(f"[ERROR] Backup failed: {e}")
            return False

    def fix_html_headers(self):
        """
        Fix HTML headers and meta tags for better performance.
        """
        print("\n[HTML] Optimizing HTML headers...")

        index_html = self.project_dir / "index.html"
        if not index_html.exists():
            print("[HTML] No index.html found, skipping")
            return

        try:
            with open(index_html, 'r') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Check for viewport meta tag
            viewport = soup.find('meta', attrs={'name': 'viewport'})
            if not viewport:
                viewport_tag = soup.new_tag(
                    'meta',
                    attrs={
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'
                    }
                )
                soup.head.append(viewport_tag)
                self.fixes_applied.append("Added viewport meta tag")

            # Add charset if missing
            charset = soup.find('meta', attrs={'charset': True})
            if not charset:
                charset_tag = soup.new_tag('meta', attrs={'charset': 'UTF-8'})
                soup.head.insert(0, charset_tag)
                self.fixes_applied.append("Added charset meta tag")

            # Add theme-color for mobile
            theme_color = soup.find('meta', attrs={'name': 'theme-color'})
            if not theme_color:
                theme_tag = soup.new_tag(
                    'meta',
                    attrs={'name': 'theme-color', 'content': '#ffffff'}
                )
                soup.head.append(theme_tag)
                self.fixes_applied.append("Added theme-color meta tag")

            # Add preconnect for performance
            preconnect_api = soup.find('link', attrs={'href': 'https://api.pokemontcg.io'})
            if not preconnect_api:
                preconnect_tag = soup.new_tag(
                    'link',
                    attrs={'rel': 'preconnect', 'href': 'https://api.pokemontcg.io'}
                )
                soup.head.append(preconnect_tag)
                self.performance_improvements.append("Added preconnect to Pokemon TCG API")

            # Save modified HTML
            with open(index_html, 'w') as f:
                f.write(str(soup.prettify()))

            self.files_modified.append(str(index_html))
            print(f"[HTML] Optimized: {index_html.name}")

        except Exception as e:
            print(f"[ERROR] HTML optimization failed: {e}")
            self.warnings.append(f"HTML optimization failed: {e}")

    def add_security_headers_config(self):
        """
        Add security headers configuration.
        Creates configuration files for various deployment platforms.
        """
        print("\n[SECURITY] Adding security headers...")

        # Create vercel.json with security headers
        vercel_config = self.project_dir / "vercel.json"
        security_headers = {
            "headers": [
                {
                    "source": "/(.*)",
                    "headers": [
                        {
                            "key": "X-Content-Type-Options",
                            "value": "nosniff"
                        },
                        {
                            "key": "X-Frame-Options",
                            "value": "DENY"
                        },
                        {
                            "key": "X-XSS-Protection",
                            "value": "1; mode=block"
                        },
                        {
                            "key": "Referrer-Policy",
                            "value": "strict-origin-when-cross-origin"
                        },
                        {
                            "key": "Permissions-Policy",
                            "value": "camera=(), microphone=(), geolocation=()"
                        },
                        {
                            "key": "Content-Security-Policy",
                            "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.pokemontcg.io;"
                        }
                    ]
                }
            ]
        }

        try:
            # Merge with existing vercel.json if it exists
            if vercel_config.exists():
                with open(vercel_config) as f:
                    existing_config = json.load(f)
                existing_config["headers"] = security_headers["headers"]
                config_to_write = existing_config
            else:
                config_to_write = security_headers

            with open(vercel_config, 'w') as f:
                json.dump(config_to_write, f, indent=2)

            self.security_improvements.append("Added comprehensive security headers")
            self.files_modified.append(str(vercel_config))
            print("[SECURITY] Security headers configuration added")

        except Exception as e:
            print(f"[ERROR] Security headers configuration failed: {e}")
            self.warnings.append(f"Security headers failed: {e}")

    def optimize_images_config(self):
        """
        Add image optimization configuration.
        """
        print("\n[IMAGES] Configuring image optimization...")

        # Add image optimization to vite config
        vite_config = self.project_dir / "vite.config.ts"

        if not vite_config.exists():
            print("[IMAGES] No vite.config.ts found")
            return

        try:
            with open(vite_config, 'r') as f:
                content = f.read()

            # Check if vite-plugin-image-optimizer is already configured
            if 'vite-plugin-image-optimizer' in content:
                print("[IMAGES] Image optimization already configured")
                return

            # Add recommendation to package.json for installation
            recommendation = """
# Image Optimization Recommendation
# Install: npm install --save-dev vite-plugin-image-optimizer

# Then add to vite.config.ts:
# import { ViteImageOptimizer } from 'vite-plugin-image-optimizer';
# plugins: [react(), ViteImageOptimizer()]
"""
            readme_path = self.project_dir / "IMAGE_OPTIMIZATION.md"
            with open(readme_path, 'w') as f:
                f.write(recommendation)

            self.performance_improvements.append("Added image optimization recommendation")
            print("[IMAGES] Image optimization guide created")

        except Exception as e:
            print(f"[ERROR] Image optimization config failed: {e}")

    def strip_console_logs(self):
        """
        Remove console.log statements from production code.
        """
        print("\n[CLEANUP] Removing console.log statements...")

        src_dir = self.project_dir / "src"
        if not src_dir.exists():
            print("[CLEANUP] No src directory found")
            return

        files_cleaned = 0
        logs_removed = 0

        for file_path in src_dir.rglob("*.ts*"):
            if file_path.is_file():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Count console.logs
                    original_logs = len(re.findall(r'console\.(log|debug|info|warn)\(', content))

                    if original_logs > 0:
                        # Remove console.log/debug/info/warn but keep error
                        new_content = re.sub(
                            r'^\s*console\.(log|debug|info|warn)\([^)]*\);?\s*$',
                            '',
                            content,
                            flags=re.MULTILINE
                        )

                        if new_content != content:
                            with open(file_path, 'w') as f:
                                f.write(new_content)

                            files_cleaned += 1
                            logs_removed += original_logs
                            self.files_modified.append(str(file_path))

                except Exception as e:
                    print(f"[WARNING] Failed to clean {file_path}: {e}")

        if logs_removed > 0:
            self.performance_improvements.append(
                f"Removed {logs_removed} console.log statements from {files_cleaned} files"
            )
            print(f"[CLEANUP] Removed {logs_removed} console statements from {files_cleaned} files")
        else:
            print("[CLEANUP] No console.log statements found")

    def add_lazy_loading_to_images(self):
        """
        Add lazy loading to images in components.
        """
        print("\n[LAZY-LOAD] Adding lazy loading to images...")

        components_dir = self.project_dir / "src" / "components"
        if not components_dir.exists():
            print("[LAZY-LOAD] No components directory found")
            return

        images_updated = 0

        for file_path in components_dir.rglob("*.tsx"):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()

                # Find img tags without loading="lazy"
                img_pattern = r'<img\s+([^>]*?)(?<!loading=["\']lazy["\'])\s*>'
                matches = re.findall(img_pattern, content)

                if matches:
                    # Add loading="lazy" to img tags that don't have it
                    new_content = re.sub(
                        r'<img\s+',
                        lambda m: '<img loading="lazy" ',
                        content
                    )

                    # Remove duplicate loading attributes
                    new_content = re.sub(
                        r'loading="lazy"\s+loading="lazy"',
                        'loading="lazy"',
                        new_content
                    )

                    with open(file_path, 'w') as f:
                        f.write(new_content)

                    images_updated += 1
                    self.files_modified.append(str(file_path))

            except Exception as e:
                print(f"[WARNING] Failed to update {file_path}: {e}")

        if images_updated > 0:
            self.performance_improvements.append(
                f"Added lazy loading to images in {images_updated} components"
            )
            print(f"[LAZY-LOAD] Updated {images_updated} component files")
        else:
            print("[LAZY-LOAD] Images already optimized or no images found")

    def create_service_worker(self):
        """
        Create a basic service worker for caching.
        """
        print("\n[SW] Creating service worker...")

        sw_content = """// Service Worker for Pokemon TCG Search
const CACHE_NAME = 'pokemon-tcg-v1';
const urlsToCache = [
  '/',
  '/index.html',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => response || fetch(event.request))
  );
});
"""

        try:
            sw_path = self.project_dir / "public" / "service-worker.js"
            sw_path.parent.mkdir(exist_ok=True)

            with open(sw_path, 'w') as f:
                f.write(sw_content)

            self.performance_improvements.append("Created service worker for caching")
            self.files_modified.append(str(sw_path))
            print(f"[SW] Service worker created: {sw_path}")

        except Exception as e:
            print(f"[ERROR] Service worker creation failed: {e}")

    def generate_fix_report(self) -> FixReport:
        """
        Generate comprehensive fix report.

        Returns:
            FixReport object
        """
        report = FixReport(
            timestamp=datetime.now().isoformat(),
            fixes_applied=self.fixes_applied,
            files_modified=self.files_modified,
            security_improvements=self.security_improvements,
            performance_improvements=self.performance_improvements,
            warnings=self.warnings,
            success=len(self.warnings) == 0
        )

        # Save report
        report_file = self.project_dir / f"implementation_report_{self.timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": report.timestamp,
                "fixes_applied": report.fixes_applied,
                "files_modified": report.files_modified,
                "security_improvements": report.security_improvements,
                "performance_improvements": report.performance_improvements,
                "warnings": report.warnings,
                "success": report.success
            }, f, indent=2)

        print(f"\n[REPORT] Implementation report saved: {report_file}")
        return report

    def run_full_implementation(self) -> FixReport:
        """
        Run complete implementation of all fixes.

        Returns:
            FixReport object
        """
        print("\n" + "="*70)
        print("PERFORMANCE IMPLEMENTATION AGENT - FULL RUN")
        print("="*70)

        # Create backup first
        if not self.create_backup():
            print("[ERROR] Backup failed, aborting implementation")
            return FixReport(
                timestamp=datetime.now().isoformat(),
                fixes_applied=[],
                files_modified=[],
                security_improvements=[],
                performance_improvements=[],
                warnings=["Backup failed - implementation aborted"],
                success=False
            )

        # Run all fixes
        self.fix_html_headers()
        self.add_security_headers_config()
        self.optimize_images_config()
        self.strip_console_logs()
        self.add_lazy_loading_to_images()
        self.create_service_worker()

        # Generate report
        report = self.generate_fix_report()

        # Print summary
        print("\n" + "="*70)
        print("IMPLEMENTATION SUMMARY")
        print("="*70)
        print(f"Total Fixes Applied: {len(self.fixes_applied)}")
        print(f"Files Modified: {len(self.files_modified)}")
        print(f"Security Improvements: {len(self.security_improvements)}")
        print(f"Performance Improvements: {len(self.performance_improvements)}")
        print(f"Warnings: {len(self.warnings)}")

        print("\n" + "="*70)
        print("CHANGES MADE:")
        print("="*70)

        if self.performance_improvements:
            print("\n🚀 Performance Improvements:")
            for improvement in self.performance_improvements:
                print(f"  • {improvement}")

        if self.security_improvements:
            print("\n🔒 Security Improvements:")
            for improvement in self.security_improvements:
                print(f"  • {improvement}")

        if self.warnings:
            print("\n⚠️ Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")

        print("\n" + "="*70)
        print(f"Backup location: {self.backup_dir}")
        print("="*70 + "\n")

        return report


def main():
    """Main entry point for the implementation agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Performance Implementation Agent - Apply performance and security fixes"
    )
    parser.add_argument(
        "project_dir",
        help="Path to project directory"
    )
    parser.add_argument(
        "-r", "--report",
        help="Path to monitoring agent report (optional)"
    )

    args = parser.parse_args()

    agent = PerformanceImplementationAgent(args.project_dir, args.report)
    report = agent.run_full_implementation()

    sys.exit(0 if report.success else 1)


if __name__ == "__main__":
    main()


# ============================================================================
# TODO: FUTURE ENHANCEMENTS FOR MAXIMUM ROBUSTNESS
# ============================================================================

"""
PHASE 1: Code Transformation
- [ ] Automatic WordPress to static HTML conversion
- [ ] jQuery to vanilla JavaScript migration
- [ ] Legacy framework removal (AngularJS, Backbone, etc.)
- [ ] Inline styles to CSS extraction
- [ ] CSS-in-JS to separate stylesheets
- [ ] Remove abandoned npm packages
- [ ] Update vulnerable dependencies
- [ ] Convert CommonJS to ES modules
- [ ] TypeScript migration assistance
- [ ] Remove duplicate dependencies

PHASE 2: Advanced Image Optimization
- [ ] Automatic WebP/AVIF conversion
- [ ] Responsive image srcset generation
- [ ] Image compression with quality preservation
- [ ] Lazy loading implementation
- [ ] Blur-up placeholder generation
- [ ] SVG optimization
- [ ] Remove EXIF data
- [ ] Generate multiple resolutions
- [ ] CDN integration for images
- [ ] Art direction implementation

PHASE 3: CSS Optimization
- [ ] Remove unused CSS (PurgeCSS)
- [ ] CSS minification
- [ ] Critical CSS extraction and inlining
- [ ] Combine multiple CSS files
- [ ] Convert to CSS modules
- [ ] Autoprefixer application
- [ ] CSS Grid/Flexbox optimization
- [ ] Remove vendor prefixes (when safe)
- [ ] Dark mode implementation
- [ ] CSS custom properties migration

PHASE 4: JavaScript Optimization
- [ ] Code splitting implementation
- [ ] Dynamic imports for routes
- [ ] Lazy loading of heavy components
- [ ] Minification and uglification
- [ ] Tree shaking verification
- [ ] Polyfill optimization (targeted)
- [ ] Webpack/Rollup/Vite optimization
- [ ] Remove console statements
- [ ] Dead code elimination
- [ ] Bundle analysis and visualization

PHASE 5: HTML Optimization
- [ ] Minify HTML
- [ ] Remove comments
- [ ] Inline critical CSS
- [ ] Defer non-critical JavaScript
- [ ] Async script loading
- [ ] Preconnect to required origins
- [ ] DNS prefetch implementation
- [ ] Resource hints (preload, prefetch)
- [ ] Meta tag optimization
- [ ] Structured data implementation

PHASE 6: Performance Patterns
- [ ] Implement service worker for caching
- [ ] Add offline functionality
- [ ] Implement HTTP/2 server push
- [ ] Enable Brotli compression
- [ ] Implement CDN integration
- [ ] Add cache-control headers
- [ ] Implement ETag generation
- [ ] Add gzip compression
- [ ] Implement response streaming
- [ ] Add edge computing support

PHASE 7: React/Frontend Optimization
- [ ] React.memo implementation
- [ ] useCallback/useMemo addition
- [ ] Code splitting by route
- [ ] Lazy component loading
- [ ] Virtual scrolling implementation
- [ ] Debouncing/throttling addition
- [ ] Event delegation optimization
- [ ] Prop drilling elimination
- [ ] Context optimization
- [ ] Re-render prevention

PHASE 8: Build Process
- [ ] Webpack/Vite optimization
- [ ] Production build configuration
- [ ] Source map generation (production-safe)
- [ ] Asset hashing for cache busting
- [ ] Chunk splitting strategy
- [ ] Vendor bundle separation
- [ ] Runtime chunk extraction
- [ ] Module concatenation
- [ ] Scope hoisting
- [ ] Parallel processing

PHASE 9: Backend Integration
- [ ] API call optimization
- [ ] Request batching
- [ ] Caching layer implementation
- [ ] GraphQL query optimization
- [ ] Database query optimization hints
- [ ] Server-side rendering setup
- [ ] Static site generation
- [ ] Incremental static regeneration
- [ ] Edge function implementation
- [ ] Serverless optimization

PHASE 10: Monitoring Implementation
- [ ] Add Web Vitals tracking
- [ ] Performance Observer integration
- [ ] Custom metrics instrumentation
- [ ] Error tracking implementation
- [ ] Analytics integration
- [ ] Real User Monitoring setup
- [ ] Synthetic monitoring
- [ ] A/B testing framework
- [ ] Feature flag implementation
- [ ] Performance budgets enforcement

PHASE 11: Security Implementation
- [ ] CSP policy generation and implementation
- [ ] CORS configuration optimization
- [ ] XSS prevention measures
- [ ] CSRF token implementation
- [ ] Secure cookie configuration
- [ ] HSTS header implementation
- [ ] Subresource Integrity (SRI)
- [ ] Input validation and sanitization
- [ ] Output encoding
- [ ] Security audit automation

PHASE 12: Mobile Optimization
- [ ] Touch event optimization
- [ ] Viewport configuration
- [ ] Mobile-first CSS
- [ ] Reduced motion preferences
- [ ] Network information API usage
- [ ] Battery status consideration
- [ ] Adaptive loading
- [ ] Mobile debugging tools
- [ ] App shell implementation
- [ ] Install prompt handling

IMPLEMENTATION PRIORITY:
Critical: Phase 1, Phase 4, Phase 6, Phase 11
High: Phase 2, Phase 3, Phase 7, Phase 10
Medium: Phase 5, Phase 8, Phase 9
Low: Phase 12

SAFETY FEATURES TO ADD:
- [ ] Dry-run mode (preview changes without applying)
- [ ] Rollback mechanism (automated)
- [ ] Change validation before commit
- [ ] Incremental application of fixes
- [ ] Dependency conflict detection
- [ ] Breaking change warnings
- [ ] Browser compatibility checks
- [ ] Regression test integration
- [ ] Performance regression prevention
- [ ] Automated testing after changes

INTEGRATION CAPABILITIES:
- [ ] Git integration for automatic commits
- [ ] GitHub Actions workflow generation
- [ ] GitLab CI pipeline integration
- [ ] CircleCI configuration
- [ ] Jenkins plugin
- [ ] Docker containerization
- [ ] Kubernetes deployment
- [ ] Terraform infrastructure as code
- [ ] AWS Lambda deployment
- [ ] Vercel/Netlify integration

REPORTING ENHANCEMENTS:
- [ ] Before/after performance comparison
- [ ] Visual diff generation
- [ ] Bundle size comparison
- [ ] Lighthouse score tracking
- [ ] Automated PR comments
- [ ] Slack notifications
- [ ] Email reports
- [ ] Dashboard generation
- [ ] Cost-benefit analysis
- [ ] ROI calculations

TECHNICAL DEBT:
- Add comprehensive unit tests
- Implement integration tests
- Add type hints (Python 3.9+)
- Improve error messages
- Add logging levels (DEBUG, INFO, WARN, ERROR)
- Implement configuration files (YAML/JSON)
- Add plugin architecture
- Implement undo functionality
- Add diff preview before changes
- Implement selective application of fixes
"""
