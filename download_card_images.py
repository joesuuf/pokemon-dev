#!/usr/bin/env python3
"""
Pokemon TCG Masterlist Image Downloader

This script processes the Pokemon card masterlist, downloads high-resolution
images for all cards, and updates the masterlist with download status flags.

Usage:
    python download_card_images.py [--masterlist PATH] [--output-dir PATH] [--concurrent N]

Flags:
    --masterlist PATH    Path to masterlist JSON file (default: data/masterlist.json)
    --output-dir PATH   Directory to save images (default: public/images/cards)
    --concurrent N       Number of concurrent downloads (default: 5)
    --resume             Resume from previous download state
    --verify-only        Only verify existing downloads without downloading
"""

import json
import os
import sys
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Literal
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import hashlib
import time
import random

# Download status types
DownloadStatus = Literal['downloaded', 'missing', 'needed', 'error']

# Configuration
DEFAULT_MASTERLIST_PATH = 'data/masterlist.json'
DEFAULT_OUTPUT_DIR = 'public/images/cards'
DEFAULT_CONCURRENT_DOWNLOADS = 5
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
BASE_TIMEOUT = 30  # seconds - base timeout for requests
MIN_DELAY = 0.5  # minimum delay between requests (seconds)
MAX_DELAY = 2.0  # maximum delay between requests (seconds)


class ImageDownloader:
    """Handles downloading and tracking Pokemon card images"""
    
    def __init__(
        self,
        masterlist_path: str,
        output_dir: str,
        concurrent_downloads: int = DEFAULT_CONCURRENT_DOWNLOADS
    ):
        self.masterlist_path = Path(masterlist_path)
        self.output_dir = Path(output_dir)
        self.concurrent_downloads = concurrent_downloads
        self.stats = {
            'total': 0,
            'downloaded': 0,
            'missing': 0,
            'needed': 0,
            'error': 0,
            'skipped': 0
        }
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_masterlist(self) -> List[Dict]:
        """Load masterlist JSON file"""
        if not self.masterlist_path.exists():
            print(f"Error: Masterlist file not found: {self.masterlist_path}")
            sys.exit(1)
        
        print(f"Loading masterlist from {self.masterlist_path}...")
        with open(self.masterlist_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle both array format and object with 'data' key
        if isinstance(data, dict) and 'data' in data:
            cards = data['data']
        elif isinstance(data, list):
            cards = data
        else:
            print("Error: Invalid masterlist format")
            sys.exit(1)
        
        print(f"Loaded {len(cards)} cards from masterlist")
        return cards
    
    def save_masterlist(self, cards: List[Dict]):
        """Save updated masterlist back to file"""
        print(f"\nSaving updated masterlist to {self.masterlist_path}...")
        
        # Ensure parent directory exists
        self.masterlist_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Backup original file if it exists
        if self.masterlist_path.exists():
            backup_path = self.masterlist_path.with_suffix('.json.backup')
            print(f"Creating backup: {backup_path}")
            import shutil
            shutil.copy2(self.masterlist_path, backup_path)
        
        # Save updated masterlist
        with open(self.masterlist_path, 'w', encoding='utf-8') as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
        
        print("Masterlist saved successfully")
    
    def get_image_filename(self, card: Dict) -> str:
        """Generate filename for card image based on card ID"""
        card_id = card.get('id', '')
        # Sanitize card ID for filename
        safe_id = card_id.replace('/', '_').replace('\\', '_')
        return f"{safe_id}.jpg"
    
    def get_image_path(self, card: Dict) -> Path:
        """Get full path to local image file"""
        filename = self.get_image_filename(card)
        return self.output_dir / filename
    
    def check_image_exists(self, card: Dict) -> bool:
        """Check if image file already exists locally"""
        image_path = self.get_image_path(card)
        return image_path.exists() and image_path.stat().st_size > 0
    
    def download_image(self, card: Dict, retry_count: int = 0) -> bool:
        """Download image for a single card"""
        card_id = card.get('id', 'unknown')
        images = card.get('images', {})
        large_url = images.get('large')
        
        if not large_url:
            print(f"  [MISSING] Card {card_id}: No large image URL")
            return False
        
        image_path = self.get_image_path(card)
        
        # Check if already downloaded
        if self.check_image_exists(card):
            return True
        
        try:
            # Add randomized delay before download to avoid robotic behavior
            # Delay between MIN_DELAY and MAX_DELAY seconds, in 0.1 increments
            # Note: With concurrent downloads, delays overlap between threads,
            # but each request still has its own randomized timing
            delay = round(random.uniform(MIN_DELAY, MAX_DELAY), 1)
            time.sleep(delay)
            
            # Download image
            print(f"  [DOWNLOAD] {card_id} -> {image_path.name}")
            
            # Randomize timeout: 1.0x to 2.5x BASE_TIMEOUT, in 0.1 second increments
            # This varies per request to avoid robotic patterns
            timeout_multiplier = round(random.uniform(1.0, 2.5), 1)
            randomized_timeout = round(BASE_TIMEOUT * timeout_multiplier, 1)
            
            # Create request with headers to avoid blocking
            req = urllib.request.Request(
                large_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            with urllib.request.urlopen(req, timeout=randomized_timeout) as response:
                image_data = response.read()
                
                # Verify we got image data
                if len(image_data) < 1000:  # Too small to be a valid image
                    raise ValueError("Downloaded data too small")
                
                # Save image
                image_path.write_bytes(image_data)
                
                return True
        
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"  [MISSING] Card {card_id}: Image not found (404)")
                return False
            elif retry_count < MAX_RETRIES:
                print(f"  [RETRY] Card {card_id}: HTTP {e.code}, retrying...")
                time.sleep(RETRY_DELAY)
                return self.download_image(card, retry_count + 1)
            else:
                print(f"  [ERROR] Card {card_id}: HTTP {e.code} after {MAX_RETRIES} retries")
                return False
        
        except Exception as e:
            if retry_count < MAX_RETRIES:
                print(f"  [RETRY] Card {card_id}: {str(e)}, retrying...")
                time.sleep(RETRY_DELAY)
                return self.download_image(card, retry_count + 1)
            else:
                print(f"  [ERROR] Card {card_id}: {str(e)}")
                return False
    
    def update_card_status(self, card: Dict) -> DownloadStatus:
        """Update and return download status for a card"""
        images = card.get('images', {})
        large_url = images.get('large')
        
        if not large_url:
            status = 'missing'
        elif self.check_image_exists(card):
            status = 'downloaded'
        else:
            status = 'needed'
        
        # Update card with status flag
        if 'imageStatus' not in card:
            card['imageStatus'] = {}
        card['imageStatus']['large'] = status
        card['imageStatus']['updatedAt'] = datetime.now().isoformat()
        
        return status
    
    def process_card(self, card: Dict, download: bool = True) -> DownloadStatus:
        """Process a single card: check status and download if needed"""
        status = self.update_card_status(card)
        
        if status == 'needed' and download:
            if self.download_image(card):
                status = 'downloaded'
                card['imageStatus']['large'] = 'downloaded'
                card['imageStatus']['updatedAt'] = datetime.now().isoformat()
            else:
                status = 'error'
                card['imageStatus']['large'] = 'error'
        
        return status
    
    def process_masterlist(
        self,
        cards: List[Dict],
        download: bool = True,
        verify_only: bool = False
    ):
        """Process all cards in masterlist"""
        print(f"\nProcessing {len(cards)} cards...")
        print(f"Download mode: {'VERIFY ONLY' if verify_only else ('DOWNLOAD' if download else 'CHECK STATUS')}")
        print(f"Output directory: {self.output_dir}")
        print(f"Concurrent downloads: {self.concurrent_downloads}")
        
        # Randomize card order to avoid scraping in sequential order
        # This prevents robotic patterns when downloading cards
        if download and not verify_only:
            print("Randomizing card order for non-sequential scraping...")
            cards = cards.copy()  # Don't modify original list
            random.shuffle(cards)
            print(f"Cards randomized - processing in random order\n")
        else:
            print()
        
        if verify_only:
            download = False
        
        # Process cards with threading for downloads
        if download and not verify_only:
            with ThreadPoolExecutor(max_workers=self.concurrent_downloads) as executor:
                futures = {
                    executor.submit(self.process_card, card, download=True): card
                    for card in cards
                }
                
                completed = 0
                for future in as_completed(futures):
                    card = futures[future]
                    try:
                        status = future.result()
                        self.stats[status] = self.stats.get(status, 0) + 1
                        completed += 1
                        
                        if completed % 50 == 0:
                            print(f"Progress: {completed}/{len(cards)} cards processed...")
                    except Exception as e:
                        card_id = card.get('id', 'unknown')
                        print(f"  [ERROR] Card {card_id}: {str(e)}")
                        self.stats['error'] += 1
        else:
            # Just check status without downloading
            for i, card in enumerate(cards, 1):
                status = self.process_card(card, download=False)
                self.stats[status] = self.stats.get(status, 0) + 1
                
                if i % 100 == 0:
                    print(f"Progress: {i}/{len(cards)} cards checked...")
        
        self.stats['total'] = len(cards)
    
    def print_stats(self):
        """Print download statistics"""
        print("\n" + "="*60)
        print("DOWNLOAD STATISTICS")
        print("="*60)
        print(f"Total cards:           {self.stats['total']}")
        print(f"Downloaded:             {self.stats['downloaded']}")
        print(f"Needed (not downloaded): {self.stats['needed']}")
        print(f"Missing (no URL):       {self.stats['missing']}")
        print(f"Errors:                 {self.stats['error']}")
        print(f"Success rate:           {(self.stats['downloaded'] / self.stats['total'] * 100):.1f}%")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description='Download high-resolution Pokemon card images from masterlist'
    )
    parser.add_argument(
        '--masterlist',
        default=DEFAULT_MASTERLIST_PATH,
        help=f'Path to masterlist JSON file (default: {DEFAULT_MASTERLIST_PATH})'
    )
    parser.add_argument(
        '--output-dir',
        default=DEFAULT_OUTPUT_DIR,
        help=f'Directory to save images (default: {DEFAULT_OUTPUT_DIR})'
    )
    parser.add_argument(
        '--concurrent',
        type=int,
        default=DEFAULT_CONCURRENT_DOWNLOADS,
        help=f'Number of concurrent downloads (default: {DEFAULT_CONCURRENT_DOWNLOADS})'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify existing downloads without downloading new ones'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only check status without downloading or verifying'
    )
    
    args = parser.parse_args()
    
    # Validate Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    # Create downloader
    downloader = ImageDownloader(
        masterlist_path=args.masterlist,
        output_dir=args.output_dir,
        concurrent_downloads=args.concurrent
    )
    
    # Load masterlist
    cards = downloader.load_masterlist()
    
    # Process cards
    start_time = time.time()
    downloader.process_masterlist(
        cards,
        download=not args.check_only and not args.verify_only,
        verify_only=args.verify_only
    )
    elapsed_time = time.time() - start_time
    
    # Save updated masterlist
    downloader.save_masterlist(cards)
    
    # Print statistics
    downloader.print_stats()
    print(f"\nTotal time: {elapsed_time:.1f} seconds")
    print(f"Average time per card: {elapsed_time / len(cards):.2f} seconds")


if __name__ == '__main__':
    main()
