#!/bin/bash
# Generate folder size audit report for pokemon-dev workspace

echo "=== Pokemon TCG Application - Folder Size Audit ==="
echo ""
echo "Generated: $(date)"
echo ""

echo "--- Top-Level Directories ---"
du -sh */ 2>/dev/null | sort -hr | awk '{printf "%-20s %10s\n", $2, $1}'

echo ""
echo "--- Total Workspace Size ---"
du -sh . 2>/dev/null

echo ""
echo "--- File Counts ---"
echo "Total files: $(find . -type f | wc -l)"
echo "Total directories: $(find . -type d | wc -l)"
echo "TypeScript files (source): $(find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | wc -l)"
echo "Python files: $(find . -name "*.py" | grep -v node_modules | wc -l)"
echo "Markdown files: $(find . -name "*.md" | grep -v node_modules | wc -l)"
echo "JavaScript files (source): $(find . -name "*.js" | grep -v node_modules | wc -l)"
echo "CSS files: $(find . -name "*.css" | grep -v node_modules | wc -l)"

echo ""
echo "--- Frontend Versions Breakdown ---"
du -sh frontends/*/ 2>/dev/null | sort -hr | awk '{printf "%-20s %10s\n", $2, $1}'

echo ""
echo "--- Documentation Breakdown ---"
du -sh documentation/*/ 2>/dev/null | sort -hr | head -10 | awk '{printf "%-30s %10s\n", $2, $1}'

echo ""
echo "=== Audit Complete ==="
