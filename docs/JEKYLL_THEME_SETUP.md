# GitHub Pages Jekyll Theme Setup

This repository uses the **Dinky** theme for GitHub Pages.

## Theme Configuration

The theme is configured in `_config.yml`:

```yaml
remote_theme: pages-themes/dinky@v0.2.0
plugins:
  - jekyll-remote-theme
```

## Local Development

To preview the Jekyll site locally:

1. **Install Ruby dependencies:**
   ```bash
   bundle install
   ```

2. **Build and serve locally:**
   ```bash
   bundle exec jekyll serve
   ```

3. **View site:**
   Open http://localhost:4000 in your browser

## Deployment

The site is automatically deployed via GitHub Actions when you push to the `main` or `master` branch.

The workflow `.github/workflows/deploy-jekyll-pages.yml` will:
1. Install Ruby and Jekyll dependencies
2. Build the Jekyll site with the Dinky theme
3. Deploy to GitHub Pages

## Customization

### Custom Styles

To add custom CSS, create `/assets/css/style.scss`:

```scss
---
---

@import "{{ site.theme }}";

/* Your custom styles here */
```

### Custom Layouts

To override the default layout, copy `_layouts/default.html` from the theme and customize it.

### Configuration Variables

Edit `_config.yml` to customize:
- `title`: Site title
- `description`: Site description
- `show_downloads`: Show/hide download links

## Theme Documentation

For more information about the Dinky theme:
- [Theme Repository](https://github.com/pages-themes/dinky)
- [Live Preview](http://pages-themes.github.io/dinky)
