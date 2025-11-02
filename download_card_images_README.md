# Pokemon Card Image Downloader - README

## Overview

The `download_card_images.py` script processes the Pokemon card masterlist, downloads high-resolution images for all cards, and updates the masterlist with download status flags.

## Features

- Downloads high-resolution card images from Pokemon TCG API
- Tracks download status: `downloaded`, `missing`, `needed`, or `error`
- Concurrent downloads for faster processing
- Resume capability (can verify existing downloads)
- Updates masterlist JSON with image status flags
- Creates backups before modifying masterlist

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)
- Internet connection for downloading images
- Write access to masterlist file and image output directory

## Usage

### Basic Usage

```bash
python download_card_images.py
```

This will:
- Load masterlist from `data/masterlist.json`
- Download images to `public/images/cards/`
- Update masterlist with download status flags

### Command Line Options

```bash
python download_card_images.py [OPTIONS]
```

Options:
- `--masterlist PATH` - Path to masterlist JSON file (default: `data/masterlist.json`)
- `--output-dir PATH` - Directory to save images (default: `public/images/cards`)
- `--concurrent N` - Number of concurrent downloads (default: 5)
- `--verify-only` - Only verify existing downloads without downloading new ones
- `--check-only` - Only check status without downloading or verifying

### Examples

```bash
# Use custom masterlist location
python download_card_images.py --masterlist data/pokemon-cards.json

# Save images to different directory
python download_card_images.py --output-dir static/card-images

# Use more concurrent downloads (faster but more resource-intensive)
python download_card_images.py --concurrent 10

# Verify existing downloads only
python download_card_images.py --verify-only

# Check status without downloading
python download_card_images.py --check-only
```

## Masterlist Format

The script expects a masterlist JSON file with an array of Pokemon card objects. Each card should have:
- `id`: Unique card identifier
- `images.large`: URL to high-resolution image

After processing, each card will have an `imageStatus` field added:

```json
{
  "id": "base1-1",
  "name": "Alakazam",
  "images": {
    "large": "https://images.pokemontcg.io/base1/1_hires.png"
  },
  "imageStatus": {
    "large": "downloaded",
    "updatedAt": "2025-01-15T10:30:00"
  }
}
```

### Image Status Values

- `downloaded`: Image successfully downloaded and saved locally
- `missing`: No image URL available for this card
- `needed`: Image URL exists but not yet downloaded
- `error`: Error occurred during download

## Image Storage

Images are saved with filenames based on card IDs:
- Card ID: `base1-1` ? Filename: `base1-1.jpg`
- Card ID: `base1-1/2023` ? Filename: `base1-1_2023.jpg` (special characters replaced)

Images are stored in: `public/images/cards/` (or custom `--output-dir`)

## Integration with Frontend

The TypeScript code can check `imageStatus` and use local images when available:

```typescript
import { getCardImageUrl } from './services/masterlistService';

// Get image URL (prefers local if downloaded)
const imageUrl = getCardImageUrl(card, 'large');
```

## Performance

- Typical download speed: ~5-10 cards/second (depends on network)
- With 1000 cards: ~2-3 minutes with 5 concurrent downloads
- Storage: ~50-200KB per image (varies by card)

## Error Handling

- Retries failed downloads up to 3 times
- Creates backup of masterlist before updating
- Continues processing even if some downloads fail
- Reports detailed statistics at the end

## Notes

- First run will download all images (may take time)
- Subsequent runs will only download missing images
- Use `--verify-only` to check status without downloading
- Masterlist backup is created as `.json.backup`
