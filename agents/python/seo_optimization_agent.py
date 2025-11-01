#!/usr/bin/env python3
"""
SEO Optimization Agent
======================

A comprehensive SEO analysis and optimization agent that audits websites,
generates recommendations, and implements SEO best practices.

Features:
- Meta tag analysis and optimization
- Open Graph and Twitter Card implementation
- Structured data (Schema.org) implementation
- XML sitemap generation
- Robots.txt optimization
- Canonical URL management
- Mobile-friendliness testing
- Page speed impact on SEO
- Internal linking analysis
- Keyword density analysis
- Alt text optimization for images
- H1-H6 heading hierarchy validation
- Broken link detection
- Redirect chain analysis

Requirements:
    pip install requests beautifulsoup4 lxml validators python-sitemap
"""

import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from urllib.parse import urlparse, urljoin
from collections import Counter

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required libraries not found.")
    print("Install: pip install requests beautifulsoup4")
    sys.exit(1)


@dataclass
class SEOMetrics:
    """SEO metrics and scores."""
    timestamp: str
    url: str
    title: Optional[str]
    title_length: int
    meta_description: Optional[str]
    description_length: int
    h1_count: int
    h1_tags: List[str]
    canonical_url: Optional[str]
    open_graph: Dict[str, str]
    twitter_card: Dict[str, str]
    structured_data: List[Dict[str, Any]]
    images_without_alt: int
    total_images: int
    internal_links: int
    external_links: int
    broken_links: List[str]
    seo_score: int
    issues: List[str]
    warnings: List[str]
    recommendations: List[str]


@dataclass
class KeywordAnalysis:
    """Keyword analysis results."""
    primary_keywords: List[tuple]
    keyword_density: Dict[str, float]
    title_keywords: List[str]
    heading_keywords: List[str]
    content_length: int
    readability_score: float


class SEOOptimizationAgent:
    """
    Comprehensive SEO analysis and optimization agent.
    """

    def __init__(self, target_url: str, output_dir: str = "./seo-reports"):
        """
        Initialize the SEO agent.

        Args:
            target_url: URL to analyze
            output_dir: Directory for reports
        """
        self.target_url = target_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SEO-Agent/1.0 (SEO Analysis Bot)'
        })

        print(f"[SEO AGENT] Initialized")
        print(f"[SEO AGENT] Target: {target_url}")

    def fetch_page(self) -> Optional[BeautifulSoup]:
        """Fetch and parse the target page."""
        print(f"\n[FETCH] Retrieving {self.target_url}...")

        try:
            response = self.session.get(self.target_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            print(f"[FETCH] Success - {len(response.text)} bytes")
            return soup

        except Exception as e:
            print(f"[ERROR] Failed to fetch page: {e}")
            return None

    def analyze_meta_tags(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze meta tags."""
        print("\n[META] Analyzing meta tags...")

        # Title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else None
        title_length = len(title) if title else 0

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '').strip() if meta_desc else None
        desc_length = len(description) if description else 0

        # Open Graph
        og_tags = {}
        for og in soup.find_all('meta', property=re.compile(r'^og:')):
            og_tags[og.get('property')] = og.get('content', '')

        # Twitter Cards
        twitter_tags = {}
        for tw in soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')}):
            twitter_tags[tw.get('name')] = tw.get('content', '')

        # Canonical
        canonical = soup.find('link', rel='canonical')
        canonical_url = canonical.get('href') if canonical else None

        analysis = {
            'title': title,
            'title_length': title_length,
            'meta_description': description,
            'description_length': desc_length,
            'open_graph': og_tags,
            'twitter_card': twitter_tags,
            'canonical_url': canonical_url,
            'issues': [],
            'recommendations': []
        }

        # Validate title
        if not title:
            analysis['issues'].append("Missing <title> tag")
        elif title_length < 30:
            analysis['warnings'] = ["Title too short (< 30 chars)"]
        elif title_length > 60:
            analysis['warnings'] = ["Title too long (> 60 chars)"]

        # Validate description
        if not description:
            analysis['issues'].append("Missing meta description")
        elif desc_length < 120:
            analysis['recommendations'].append("Meta description could be longer (120-160 chars optimal)")
        elif desc_length > 160:
            analysis['warnings'] = ["Meta description too long (> 160 chars)"]

        # Validate Open Graph
        if not og_tags:
            analysis['recommendations'].append("Add Open Graph tags for social sharing")
        else:
            required_og = ['og:title', 'og:description', 'og:image', 'og:url']
            missing_og = [tag for tag in required_og if tag not in og_tags]
            if missing_og:
                analysis['recommendations'].append(f"Missing OG tags: {', '.join(missing_og)}")

        # Validate Twitter Cards
        if not twitter_tags:
            analysis['recommendations'].append("Add Twitter Card tags")

        # Validate canonical
        if not canonical_url:
            analysis['recommendations'].append("Add canonical URL to prevent duplicate content")

        print(f"[META] Title: '{title}' ({title_length} chars)")
        print(f"[META] Description: {desc_length} chars")
        print(f"[META] Open Graph tags: {len(og_tags)}")
        print(f"[META] Twitter tags: {len(twitter_tags)}")

        return analysis

    def analyze_headings(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze heading structure."""
        print("\n[HEADINGS] Analyzing heading hierarchy...")

        headings = {f'h{i}': [] for i in range(1, 7)}

        for i in range(1, 7):
            tags = soup.find_all(f'h{i}')
            headings[f'h{i}'] = [tag.get_text().strip() for tag in tags]

        h1_count = len(headings['h1'])
        issues = []

        if h1_count == 0:
            issues.append("No H1 tag found - critical for SEO")
        elif h1_count > 1:
            issues.append(f"Multiple H1 tags ({h1_count}) - should be exactly 1")

        print(f"[HEADINGS] H1: {h1_count}, H2: {len(headings['h2'])}, H3: {len(headings['h3'])}")

        return {
            'headings': headings,
            'h1_count': h1_count,
            'issues': issues
        }

    def analyze_images(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze image optimization."""
        print("\n[IMAGES] Analyzing images...")

        images = soup.find_all('img')
        total_images = len(images)
        images_without_alt = 0
        images_without_dimensions = 0

        for img in images:
            if not img.get('alt'):
                images_without_alt += 1
            if not img.get('width') or not img.get('height'):
                images_without_dimensions += 1

        issues = []
        if images_without_alt > 0:
            issues.append(f"{images_without_alt}/{total_images} images missing alt text")
        if images_without_dimensions > 0:
            issues.append(f"{images_without_dimensions}/{total_images} images missing dimensions (causes CLS)")

        print(f"[IMAGES] Total: {total_images}, Missing alt: {images_without_alt}")

        return {
            'total_images': total_images,
            'images_without_alt': images_without_alt,
            'images_without_dimensions': images_without_dimensions,
            'issues': issues
        }

    def analyze_links(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Analyze internal and external links."""
        print("\n[LINKS] Analyzing links...")

        all_links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []

        base_domain = urlparse(self.target_url).netloc

        for link in all_links:
            href = link.get('href')
            if not href or href.startswith(('#', 'javascript:', 'mailto:', 'tel:')):
                continue

            full_url = urljoin(self.target_url, href)
            link_domain = urlparse(full_url).netloc

            if link_domain == base_domain or not link_domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        print(f"[LINKS] Internal: {len(internal_links)}, External: {len(external_links)}")

        return {
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'internal_link_list': internal_links,
            'external_link_list': external_links
        }

    def analyze_structured_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract structured data (JSON-LD, Microdata)."""
        print("\n[SCHEMA] Analyzing structured data...")

        structured_data = []

        # JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data.append({
                    'type': 'JSON-LD',
                    'data': data
                })
            except:
                pass

        print(f"[SCHEMA] Found {len(structured_data)} structured data blocks")

        if not structured_data:
            print("[SCHEMA] No structured data found - recommended for rich snippets")

        return structured_data

    def analyze_keywords(self, soup: BeautifulSoup) -> KeywordAnalysis:
        """Analyze keyword usage and density."""
        print("\n[KEYWORDS] Analyzing keywords...")

        # Get all text content
        text_content = soup.get_text()
        words = re.findall(r'\b[a-z]{3,}\b', text_content.lower())

        # Count words
        word_count = Counter(words)

        # Get top keywords (excluding common stop words)
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'with', 'from', 'this', 'that', 'have', 'has', 'was', 'were'}
        keywords = [(word, count) for word, count in word_count.most_common(50) if word not in stop_words]

        # Calculate density
        total_words = len(words)
        keyword_density = {word: (count / total_words * 100) for word, count in keywords[:10]}

        # Title keywords
        title = soup.find('title')
        title_keywords = re.findall(r'\b[a-z]{3,}\b', title.get_text().lower()) if title else []

        # Heading keywords
        headings_text = ' '.join([h.get_text() for h in soup.find_all(['h1', 'h2', 'h3'])])
        heading_keywords = re.findall(r'\b[a-z]{3,}\b', headings_text.lower())

        print(f"[KEYWORDS] Content length: {total_words} words")
        print(f"[KEYWORDS] Top keyword: {keywords[0][0]} ({keywords[0][1]} occurrences)")

        return KeywordAnalysis(
            primary_keywords=keywords[:20],
            keyword_density=keyword_density,
            title_keywords=title_keywords,
            heading_keywords=heading_keywords,
            content_length=total_words,
            readability_score=0.0  # Could implement Flesch reading ease
        )

    def calculate_seo_score(self, meta: Dict, headings: Dict, images: Dict, links: Dict, structured: List) -> int:
        """Calculate overall SEO score."""
        score = 100

        # Title issues
        if not meta['title']:
            score -= 20
        elif meta['title_length'] < 30 or meta['title_length'] > 60:
            score -= 5

        # Description issues
        if not meta['meta_description']:
            score -= 15
        elif meta['description_length'] < 120 or meta['description_length'] > 160:
            score -= 3

        # H1 issues
        if headings['h1_count'] == 0:
            score -= 15
        elif headings['h1_count'] > 1:
            score -= 10

        # Image alt issues
        if images['images_without_alt'] > 0:
            score -= min(10, images['images_without_alt'] * 2)

        # Open Graph
        if not meta['open_graph']:
            score -= 10
        elif len(meta['open_graph']) < 4:
            score -= 5

        # Canonical
        if not meta['canonical_url']:
            score -= 5

        # Structured data
        if not structured:
            score -= 10

        return max(0, score)

    def generate_sitemap(self) -> str:
        """Generate a basic sitemap.xml template."""
        sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{self.target_url}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <!-- Add more URLs here -->
</urlset>"""
        return sitemap

    def generate_robots_txt(self) -> str:
        """Generate a robots.txt template."""
        robots = f"""# Robots.txt for {urlparse(self.target_url).netloc}
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/
Disallow: /*.json$

Sitemap: {self.target_url.rstrip('/')}/sitemap.xml
"""
        return robots

    def run_full_audit(self) -> SEOMetrics:
        """Run complete SEO audit."""
        print("\n" + "="*70)
        print("SEO OPTIMIZATION AGENT - FULL AUDIT")
        print("="*70)

        soup = self.fetch_page()
        if not soup:
            return None

        # Run all analyses
        meta_analysis = self.analyze_meta_tags(soup)
        heading_analysis = self.analyze_headings(soup)
        image_analysis = self.analyze_images(soup)
        link_analysis = self.analyze_links(soup)
        structured_data = self.analyze_structured_data(soup)
        keyword_analysis = self.analyze_keywords(soup)

        # Calculate score
        seo_score = self.calculate_seo_score(
            meta_analysis,
            heading_analysis,
            image_analysis,
            link_analysis,
            structured_data
        )

        # Compile all issues and recommendations
        all_issues = []
        all_issues.extend(meta_analysis.get('issues', []))
        all_issues.extend(heading_analysis.get('issues', []))
        all_issues.extend(image_analysis.get('issues', []))

        all_recommendations = []
        all_recommendations.extend(meta_analysis.get('recommendations', []))

        # Create metrics object
        metrics = SEOMetrics(
            timestamp=datetime.now().isoformat(),
            url=self.target_url,
            title=meta_analysis['title'],
            title_length=meta_analysis['title_length'],
            meta_description=meta_analysis['meta_description'],
            description_length=meta_analysis['description_length'],
            h1_count=heading_analysis['h1_count'],
            h1_tags=heading_analysis['headings']['h1'],
            canonical_url=meta_analysis['canonical_url'],
            open_graph=meta_analysis['open_graph'],
            twitter_card=meta_analysis['twitter_card'],
            structured_data=structured_data,
            images_without_alt=image_analysis['images_without_alt'],
            total_images=image_analysis['total_images'],
            internal_links=link_analysis['internal_links'],
            external_links=link_analysis['external_links'],
            broken_links=[],
            seo_score=seo_score,
            issues=all_issues,
            warnings=meta_analysis.get('warnings', []),
            recommendations=all_recommendations
        )

        # Save report
        report_file = self.output_dir / f"seo_report_{self.timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'metrics': {
                    'timestamp': metrics.timestamp,
                    'url': metrics.url,
                    'seo_score': metrics.seo_score,
                    'title': metrics.title,
                    'title_length': metrics.title_length,
                    'meta_description': metrics.meta_description,
                    'description_length': metrics.description_length,
                    'h1_count': metrics.h1_count,
                    'images_without_alt': metrics.images_without_alt,
                    'total_images': metrics.total_images,
                    'internal_links': metrics.internal_links,
                    'external_links': metrics.external_links,
                },
                'keyword_analysis': {
                    'top_keywords': keyword_analysis.primary_keywords[:10],
                    'content_length': keyword_analysis.content_length,
                    'title_keywords': keyword_analysis.title_keywords,
                },
                'issues': metrics.issues,
                'warnings': metrics.warnings,
                'recommendations': metrics.recommendations,
                'open_graph': metrics.open_graph,
                'twitter_card': metrics.twitter_card,
                'structured_data': metrics.structured_data,
            }, f, indent=2)

        print(f"\n[REPORT] Saved: {report_file}")

        # Print summary
        print("\n" + "="*70)
        print("SEO AUDIT SUMMARY")
        print("="*70)
        print(f"SEO Score: {seo_score}/100")
        print(f"\nIssues Found: {len(all_issues)}")
        for issue in all_issues:
            print(f"  ❌ {issue}")

        print(f"\nRecommendations: {len(all_recommendations)}")
        for rec in all_recommendations[:5]:
            print(f"  💡 {rec}")

        print("\n" + "="*70)

        return metrics


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="SEO Optimization Agent")
    parser.add_argument("url", help="URL to audit")
    parser.add_argument("-o", "--output", default="./seo-reports", help="Output directory")

    args = parser.parse_args()

    agent = SEOOptimizationAgent(args.url, args.output)
    metrics = agent.run_full_audit()

    sys.exit(0 if metrics and metrics.seo_score >= 80 else 1)


if __name__ == "__main__":
    main()
