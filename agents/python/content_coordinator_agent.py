#!/usr/bin/env python3
"""
Content Coordinator Agent
==========================

An intelligent content coordination agent that analyzes existing blogs, repurposes content,
generates new content ideas, and creates social media posts with weekly themes.

Features:
- Blog content analysis and categorization
- Content repurposing (blog → social posts, series, pillars)
- New blog idea generation from repository
- Weekly themed social media planning
- LinkedIn, Twitter, Instagram post generation
- Content pillar identification
- Blog series planning
- Content gap analysis
- Trending topic integration
- Content calendar generation

Requirements:
    pip install openai anthropic requests markdown beautifulsoup4 python-frontmatter
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Tuple
from collections import defaultdict, Counter

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: beautifulsoup4 not found. Install: pip install beautifulsoup4")
    sys.exit(1)


@dataclass
class BlogPost:
    """Represents a blog post."""
    title: str
    content: str
    file_path: str
    word_count: int
    topics: List[str]
    keywords: List[str]
    publish_date: Optional[str]
    category: Optional[str]
    tags: List[str] = field(default_factory=list)
    excerpt: str = ""


@dataclass
class SocialPost:
    """Represents a social media post."""
    platform: str  # linkedin, twitter, instagram
    content: str
    hashtags: List[str]
    media_suggestion: Optional[str]
    cta: str
    post_date: str
    theme: str


@dataclass
class ContentPillar:
    """Content pillar for organizing topics."""
    name: str
    description: str
    related_posts: List[str]
    subtopics: List[str]
    target_audience: str


@dataclass
class ContentCalendar:
    """Weekly content calendar."""
    week_of: str
    theme: str
    blog_posts: List[BlogPost]
    social_posts: List[SocialPost]
    content_pillars: List[str]


class ContentCoordinatorAgent:
    """
    Intelligent content coordinator that repurposes and plans content.
    """

    def __init__(self, blog_dir: str, ideas_repo: str, output_dir: str = "./content-plans"):
        """
        Initialize the content coordinator.

        Args:
            blog_dir: Directory containing existing blog posts
            ideas_repo: File or directory containing blog ideas and archived posts
            output_dir: Directory for output plans and calendars
        """
        self.blog_dir = Path(blog_dir)
        self.ideas_repo = Path(ideas_repo)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.existing_posts = []
        self.content_pillars = []
        self.weekly_themes = []

        print(f"[CONTENT COORDINATOR] Initialized")
        print(f"[CONTENT COORDINATOR] Blog Directory: {self.blog_dir}")
        print(f"[CONTENT COORDINATOR] Ideas Repository: {self.ideas_repo}")

    def scan_existing_blogs(self) -> List[BlogPost]:
        """Scan and analyze existing blog posts."""
        print("\n[SCAN] Scanning existing blogs...")

        posts = []

        if not self.blog_dir.exists():
            print(f"[WARNING] Blog directory not found: {self.blog_dir}")
            return posts

        # Scan for markdown and text files
        for file_path in self.blog_dir.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract title (first # heading or filename)
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else file_path.stem

                # Extract excerpt (first paragraph)
                paragraphs = re.findall(r'\n\n(.+?)\n\n', content)
                excerpt = paragraphs[0][:200] if paragraphs else ""

                # Count words
                word_count = len(content.split())

                # Extract keywords (simple approach - top words)
                words = re.findall(r'\b[a-zA-Z]{4,}\b', content.lower())
                keyword_counts = Counter(words)
                keywords = [word for word, _ in keyword_counts.most_common(10)]

                # Extract topics from headings
                topics = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)

                post = BlogPost(
                    title=title,
                    content=content,
                    file_path=str(file_path),
                    word_count=word_count,
                    topics=topics[:5],
                    keywords=keywords,
                    publish_date=None,
                    category=None,
                    excerpt=excerpt
                )

                posts.append(post)

            except Exception as e:
                print(f"[ERROR] Failed to process {file_path}: {e}")

        print(f"[SCAN] Found {len(posts)} blog posts")
        print(f"[SCAN] Total words: {sum(p.word_count for p in posts):,}")

        self.existing_posts = posts
        return posts

    def identify_content_pillars(self, posts: List[BlogPost]) -> List[ContentPillar]:
        """Identify main content pillars from existing posts."""
        print("\n[PILLARS] Identifying content pillars...")

        # Collect all keywords
        all_keywords = []
        for post in posts:
            all_keywords.extend(post.keywords)

        # Find most common themes
        keyword_counts = Counter(all_keywords)
        top_themes = [word for word, _ in keyword_counts.most_common(10)]

        # Create pillars
        pillars = []

        # Predefined pillars (can be customized)
        predefined_pillars = {
            'Technology': ['tech', 'development', 'software', 'programming', 'code'],
            'Business': ['business', 'strategy', 'growth', 'marketing', 'sales'],
            'Tutorial': ['how', 'guide', 'tutorial', 'learn', 'step'],
            'Analysis': ['analysis', 'review', 'comparison', 'performance', 'benchmark'],
        }

        for pillar_name, pillar_keywords in predefined_pillars.items():
            # Find posts matching this pillar
            matching_posts = []
            for post in posts:
                if any(kw in ' '.join(post.keywords) for kw in pillar_keywords):
                    matching_posts.append(post.title)

            if matching_posts:
                pillar = ContentPillar(
                    name=pillar_name,
                    description=f"Content focused on {pillar_name.lower()} topics",
                    related_posts=matching_posts[:10],
                    subtopics=pillar_keywords,
                    target_audience=f"{pillar_name} enthusiasts"
                )
                pillars.append(pillar)

        print(f"[PILLARS] Identified {len(pillars)} content pillars")
        for pillar in pillars:
            print(f"[PILLARS]   - {pillar.name}: {len(pillar.related_posts)} posts")

        self.content_pillars = pillars
        return pillars

    def repurpose_blog_to_social(self, blog_post: BlogPost, platform: str, theme: str) -> SocialPost:
        """Repurpose a blog post into a social media post."""

        # Platform-specific limits and styles
        platform_configs = {
            'twitter': {
                'char_limit': 280,
                'hashtag_count': 3,
                'style': 'concise'
            },
            'linkedin': {
                'char_limit': 1300,
                'hashtag_count': 5,
                'style': 'professional'
            },
            'instagram': {
                'char_limit': 2200,
                'hashtag_count': 10,
                'style': 'visual'
            }
        }

        config = platform_configs.get(platform, platform_configs['twitter'])

        # Extract key points from blog
        key_points = blog_post.topics[:3] if blog_post.topics else ['Interesting insights']

        # Create post content
        if platform == 'twitter':
            content = f"🔥 {blog_post.title}\n\n"
            content += f"Key takeaway: {blog_post.excerpt[:100]}...\n\n"
            content += "Read more 👉"

        elif platform == 'linkedin':
            content = f"{blog_post.title}\n\n"
            content += f"{blog_post.excerpt[:300]}...\n\n"
            content += "Key Points:\n"
            for i, point in enumerate(key_points, 1):
                content += f"{i}. {point}\n"
            content += "\nRead the full article to learn more."

        elif platform == 'instagram':
            content = f"✨ {blog_post.title} ✨\n\n"
            content += f"{blog_post.excerpt[:200]}...\n\n"
            content += "Swipe for key insights! 📱\n"
            content += "Link in bio for full article 🔗"

        # Generate hashtags
        hashtags = [f"#{kw.capitalize()}" for kw in blog_post.keywords[:config['hashtag_count']]]

        # CTAs
        ctas = {
            'twitter': "Retweet if you found this useful!",
            'linkedin': "What are your thoughts? Comment below!",
            'instagram': "Double tap if you agree! 💙"
        }

        post = SocialPost(
            platform=platform,
            content=content[:config['char_limit']],
            hashtags=hashtags,
            media_suggestion=f"Featured image from '{blog_post.title}'",
            cta=ctas[platform],
            post_date=datetime.now().strftime("%Y-%m-%d"),
            theme=theme
        )

        return post

    def generate_blog_series_ideas(self, pillar: ContentPillar) -> List[Dict[str, str]]:
        """Generate blog series ideas for a content pillar."""

        series_ideas = []

        # Series templates
        series_templates = [
            {
                'title': f"{pillar.name} 101: A Beginner's Guide",
                'posts': [
                    f"Introduction to {pillar.name}",
                    f"Essential {pillar.name} Concepts",
                    f"Getting Started with {pillar.name}",
                    f"Common {pillar.name} Mistakes to Avoid",
                    f"Next Steps in Your {pillar.name} Journey"
                ]
            },
            {
                'title': f"Advanced {pillar.name} Techniques",
                'posts': [
                    f"Pro Tips for {pillar.name}",
                    f"Optimizing {pillar.name} Performance",
                    f"Scaling {pillar.name} Solutions",
                    f"Case Studies in {pillar.name}"
                ]
            },
            {
                'title': f"Weekly {pillar.name} Tips",
                'posts': [
                    f"Tip #1: {subtopic}" for subtopic in pillar.subtopics[:10]
                ]
            }
        ]

        return series_templates

    def create_weekly_content_calendar(self, week_start: datetime, theme: str) -> ContentCalendar:
        """Create a weekly content calendar with themed posts."""
        print(f"\n[CALENDAR] Creating calendar for week of {week_start.strftime('%Y-%m-%d')}...")
        print(f"[CALENDAR] Theme: {theme}")

        # Select relevant blog posts
        relevant_posts = []
        if self.existing_posts:
            # Find posts matching theme
            theme_keywords = theme.lower().split()
            for post in self.existing_posts:
                post_text = ' '.join(post.keywords).lower()
                if any(kw in post_text for kw in theme_keywords):
                    relevant_posts.append(post)

            if not relevant_posts and len(self.existing_posts) >= 3:
                # Default to random selection if no matches
                relevant_posts = self.existing_posts[:3]

        # Generate social posts for each platform
        social_posts = []
        platforms = ['linkedin', 'twitter', 'instagram']

        for i, post in enumerate(relevant_posts[:7]):  # One per day
            platform = platforms[i % len(platforms)]
            post_date = week_start + timedelta(days=i)

            social_post = self.repurpose_blog_to_social(post, platform, theme)
            social_post.post_date = post_date.strftime("%Y-%m-%d %A")
            social_posts.append(social_post)

        # Identify related pillars
        related_pillars = [p.name for p in self.content_pillars if theme.lower() in p.name.lower()]

        calendar = ContentCalendar(
            week_of=week_start.strftime("%Y-%m-%d"),
            theme=theme,
            blog_posts=relevant_posts,
            social_posts=social_posts,
            content_pillars=related_pillars or [p.name for p in self.content_pillars[:2]]
        )

        print(f"[CALENDAR] Created calendar with {len(social_posts)} social posts")
        return calendar

    def generate_content_ideas(self) -> List[Dict[str, str]]:
        """Generate new content ideas based on existing content and gaps."""
        print("\n[IDEAS] Generating content ideas...")

        ideas = []

        # From pillars
        for pillar in self.content_pillars:
            series_ideas = self.generate_blog_series_ideas(pillar)
            ideas.extend([
                {
                    'type': 'blog_series',
                    'pillar': pillar.name,
                    'title': series['title'],
                    'posts': series['posts']
                }
                for series in series_ideas
            ])

        # Trending topics (mock - could integrate with real APIs)
        trending_topics = [
            "AI and Machine Learning in 2025",
            "Remote Work Best Practices",
            "Sustainable Technology",
            "Web3 and Blockchain Trends",
            "Cybersecurity Essentials"
        ]

        for topic in trending_topics:
            ideas.append({
                'type': 'trending_topic',
                'title': f"Deep Dive: {topic}",
                'angle': f"Expert perspective on {topic}"
            })

        print(f"[IDEAS] Generated {len(ideas)} content ideas")
        return ideas

    def run_full_coordination(self, weekly_themes: List[str], weeks_ahead: int = 4) -> Dict[str, Any]:
        """Run complete content coordination."""
        print("\n" + "="*70)
        print("CONTENT COORDINATOR AGENT - FULL RUN")
        print("="*70)

        # Scan existing blogs
        posts = self.scan_existing_blogs()

        # Identify pillars
        pillars = self.identify_content_pillars(posts)

        # Generate new ideas
        content_ideas = self.generate_content_ideas()

        # Create weekly calendars
        calendars = []
        today = datetime.now()

        for i in range(weeks_ahead):
            week_start = today + timedelta(weeks=i)
            theme = weekly_themes[i % len(weekly_themes)] if weekly_themes else f"Theme Week {i+1}"
            calendar = self.create_weekly_content_calendar(week_start, theme)
            calendars.append(calendar)

        # Compile report
        report = {
            'generated_at': datetime.now().isoformat(),
            'stats': {
                'existing_posts': len(posts),
                'total_words': sum(p.word_count for p in posts),
                'content_pillars': len(pillars),
                'new_ideas': len(content_ideas),
                'calendars_created': len(calendars)
            },
            'pillars': [
                {
                    'name': p.name,
                    'description': p.description,
                    'post_count': len(p.related_posts),
                    'subtopics': p.subtopics
                }
                for p in pillars
            ],
            'content_ideas': content_ideas[:20],
            'weekly_calendars': [
                {
                    'week_of': c.week_of,
                    'theme': c.theme,
                    'social_posts_count': len(c.social_posts),
                    'social_posts': [
                        {
                            'platform': sp.platform,
                            'content': sp.content[:100] + '...',
                            'hashtags': sp.hashtags,
                            'post_date': sp.post_date
                        }
                        for sp in c.social_posts
                    ]
                }
                for c in calendars
            ]
        }

        # Save report
        report_file = self.output_dir / f"content_plan_{self.timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Save individual calendars
        for calendar in calendars:
            calendar_file = self.output_dir / f"calendar_{calendar.week_of}.json"
            with open(calendar_file, 'w') as f:
                json.dump({
                    'week_of': calendar.week_of,
                    'theme': calendar.theme,
                    'social_posts': [
                        {
                            'platform': sp.platform,
                            'date': sp.post_date,
                            'content': sp.content,
                            'hashtags': sp.hashtags,
                            'cta': sp.cta
                        }
                        for sp in calendar.social_posts
                    ]
                }, f, indent=2)

        print(f"\n[REPORT] Saved: {report_file}")
        print(f"[REPORT] Created {len(calendars)} weekly calendars")

        # Print summary
        print("\n" + "="*70)
        print("CONTENT COORDINATION SUMMARY")
        print("="*70)
        print(f"Existing Posts: {len(posts)}")
        print(f"Content Pillars: {len(pillars)}")
        for pillar in pillars:
            print(f"  - {pillar.name}: {len(pillar.related_posts)} posts")

        print(f"\nWeekly Calendars Generated: {len(calendars)}")
        for calendar in calendars:
            print(f"  - Week of {calendar.week_of}: {calendar.theme} ({len(calendar.social_posts)} posts)")

        print("\n" + "="*70)

        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Content Coordinator Agent")
    parser.add_argument("blog_dir", help="Directory containing blog posts")
    parser.add_argument("ideas_repo", help="Repository of blog ideas")
    parser.add_argument(
        "-t", "--themes",
        nargs='+',
        default=["Technology", "Business", "Innovation", "Growth"],
        help="Weekly themes for content calendar"
    )
    parser.add_argument(
        "-w", "--weeks",
        type=int,
        default=4,
        help="Number of weeks ahead to plan"
    )
    parser.add_argument(
        "-o", "--output",
        default="./content-plans",
        help="Output directory"
    )

    args = parser.parse_args()

    agent = ContentCoordinatorAgent(args.blog_dir, args.ideas_repo, args.output)
    report = agent.run_full_coordination(args.themes, args.weeks)

    sys.exit(0)


if __name__ == "__main__":
    main()
