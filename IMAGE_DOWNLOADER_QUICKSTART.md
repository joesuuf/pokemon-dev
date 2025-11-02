# Pokemon Card Image Downloader - Quick Start

## What Was Created

1. **`download_card_images.py`** - Main Python script for downloading card images
2. **`download_card_images_README.md`** - Detailed documentation
3. **`download_card_images_requirements.txt`** - Dependencies (none required - uses stdlib)
4. **Updated TypeScript types** - Added `imageStatus` field to PokemonCard interface
5. **Helper function** - `getCardImageUrl()` in masterlistService.ts

## Quick Start

### 1. Create/Export Masterlist

First, you need a masterlist JSON file. The masterlist should be an array of Pokemon card objects. You can create it by:

- Exporting from your application after first search
- Or manually creating at `data/masterlist.json`

Example structure:
```json
[
  {
    "id": "base1-1",
    "name": "Alakazam",
    "images": {
      "large": "https://images.pokemontcg.io/base1/1_hires.png",
      "small": "https://images.pokemontcg.io/base1/1.png"
    }
  }
]
```

### 2. Run Download Script

```bash
# Basic usage
python download_card_images.py

# With custom paths
python download_card_images.py --masterlist data/masterlist.json --output-dir public/images/cards

# Faster downloads (more concurrent)
python download_card_images.py --concurrent 10

# Verify existing downloads only
python download_card_images.py --verify-only
```

### 3. Masterlist Updated

After running, your masterlist will have `imageStatus` flags:

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

### 4. Use in Frontend

```typescript
import { getCardImageUrl } from './services/masterlistService';

// Automatically uses local image if downloaded, otherwise remote URL
const imageUrl = getCardImageUrl(card, 'large');
```

## Image Status Values

- `downloaded` - Image successfully downloaded and saved locally
- `missing` - No image URL available for this card
- `needed` - Image URL exists but not yet downloaded
- `error` - Error occurred during download

## File Structure

```
data/
  masterlist.json              # Your Pokemon card masterlist
  masterlist.json.backup       # Backup created before update

public/
  images/
    cards/
      base1-1.jpg              # Downloaded images
      base1-2.jpg
      ...
```

## Performance Tips

- Use `--concurrent 10` for faster downloads (if your network can handle it)
- Run `--verify-only` periodically to check status without downloading
- First run downloads all images (may take time)
- Subsequent runs only download missing images

## Integration Notes

The masterlist service now includes `getCardImageUrl()` which:
- Checks `imageStatus.large` or `imageStatus.small`
- Returns local path `/images/cards/{cardId}.jpg` if downloaded
- Falls back to remote URL if not downloaded

This allows seamless switching between local and remote images!
