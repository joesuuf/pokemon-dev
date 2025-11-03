# API Mode Configuration

The app supports two API modes:

## Modes

1. **masterlist** (default) - Downloads all cards once and searches locally
   - Faster subsequent searches
   - Works offline after initial load
   - Requires initial download time

2. **direct** - Makes API calls for each search
   - Always up-to-date
   - Slower for multiple searches
   - Requires internet connection

## Configuration

Set `VITE_API_MODE` environment variable:
- `masterlist` - Use masterlist cache (default)
- `direct` - Use direct API calls

Example:
```bash
VITE_API_MODE=direct npm run build
VITE_API_MODE=masterlist npm run build
```

## GitHub Actions

The workflow defaults to `masterlist` mode. To change:
1. Add GitHub secret: `VITE_API_MODE` = `direct` or `masterlist`
2. Or modify `.github/workflows/deploy-dual-github.yml`
