#!/bin/bash
# Generate JSON audit report

echo "{"
echo "  \"generated\": \"$(date -Iseconds)\","
echo "  \"totalSize\": \"$(du -sh . 2>/dev/null | awk '{print $1}')\","
echo "  \"totalFiles\": $(find . -type f | wc -l),"
echo "  \"totalDirectories\": $(find . -type d | wc -l),"
echo "  \"topLevelDirectories\": ["
du -sh */ 2>/dev/null | sort -hr | awk '{
  size=$1
  name=$2
  gsub(/\/$/, "", name)
  printf "    {\"name\": \"%s\", \"size\": \"%s\"}", name, size
  if (NR < '$(du -sh */ 2>/dev/null | wc -l)') printf ","
  printf "\n"
}'
echo "  ],"
echo "  \"frontendVersions\": ["
du -sh frontends/*/ 2>/dev/null | sort -hr | awk '{
  size=$1
  name=$2
  gsub(/.*\//, "", name)
  gsub(/\/$/, "", name)
  printf "    {\"port\": \"%s\", \"size\": \"%s\"}", name, size
  if (NR < '$(du -sh frontends/*/ 2>/dev/null | wc -l)') printf ","
  printf "\n"
}'
echo "  ],"
echo "  \"fileTypes\": {"
echo "    \"typescript\": $(find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | wc -l),"
echo "    \"python\": $(find . -name "*.py" | grep -v node_modules | wc -l),"
echo "    \"markdown\": $(find . -name "*.md" | grep -v node_modules | wc -l),"
echo "    \"javascript\": $(find . -name "*.js" | grep -v node_modules | wc -l),"
echo "    \"css\": $(find . -name "*.css" | grep -v node_modules | wc -l)"
echo "  }"
echo "}"
