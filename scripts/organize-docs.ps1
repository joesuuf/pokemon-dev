Param(
    [string]$Root = "c:\claude-code\pokemon-dev"
)

function Ensure-Dir($path) {
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path | Out-Null
    }
}

function GitMove($src, $dest) {
    $destDir = Split-Path -Parent $dest
    Ensure-Dir (Join-Path $Root $destDir)
    Write-Host "Moving $src -> $dest"
    & git mv $src $dest
}

Set-Location $Root

# Create base directories
$baseDirs = @(
    "documentation",
    "documentation\audits\collection",
    "documentation\audits\guides",
    "documentation\guides",
    "documentation\deployment",
    "documentation\process",
    "documentation\security",
    "documentation\api",
    "documentation\ocr"
)
$baseDirs | ForEach-Object { Ensure-Dir (Join-Path $Root $_) }

# Move entire audits directory -> consolidated audits collection
if (Test-Path "audits") {
    GitMove "audits" "documentation\audits\collection"
}

# Move docs\audits subfolders -> audits guides
if (Test-Path "docs\audits") {
    GitMove "docs\audits" "documentation\audits\guides"
}

# Map root-level markdown files to new locations
$map = @{
    "API_KEYS_SETUP.md"       = "documentation\api\API_KEYS_SETUP.md";
    "AUDIT_REPORT_REACT.md"   = "documentation\audits\collection\AUDIT_REPORT_REACT.md";
    "AUDIT_SUMMARY.md"        = "documentation\audits\collection\AUDIT_SUMMARY.md";
    "SCRIPT_AUDIT_REPORT.md"  = "documentation\audits\collection\SCRIPT_AUDIT_REPORT.md";

    "BUCKET_SECURITY.md"      = "documentation\security\BUCKET_SECURITY.md";

    "DEPLOYMENT_SUMMARY.md"   = "documentation\deployment\DEPLOYMENT_SUMMARY.md";
    "DEPLOY_NOW.md"           = "documentation\deployment\DEPLOY_NOW.md";
    "GCP_DEPLOYMENT_READY.md" = "documentation\deployment\GCP_DEPLOYMENT_READY.md";
    "GCP_VS_GITHUB_PAGES.md"  = "documentation\deployment\GCP_VS_GITHUB_PAGES.md";
    "STATIC_SITE_EXPORT.md"   = "documentation\deployment\STATIC_SITE_EXPORT.md";

    "GCP_SETUP_GUIDE.md"      = "documentation\guides\GCP_SETUP_GUIDE.md";
    "WSL_SETUP.md"            = "documentation\guides\WSL_SETUP.md";
    "WSL_DEV_RUNNER.md"       = "documentation\guides\WSL_DEV_RUNNER.md";
    "DEV_PORTS_GUIDE.md"      = "documentation\guides\DEV_PORTS_GUIDE.md";
    "FRONTEND_PORTS.md"       = "documentation\guides\FRONTEND_PORTS.md";
    "DUAL_DEPLOYMENT_GUIDE.md"= "documentation\guides\DUAL_DEPLOYMENT_GUIDE.md";
    "SETUP-BOTH-REPOS.md"     = "documentation\guides\SETUP-BOTH-REPOS.md";
    "REMOTE_ACCESS.md"        = "documentation\guides\REMOTE_ACCESS.md";

    "PR-DETAILS.md"           = "documentation\process\PR-DETAILS.md";
    "PR_DESCRIPTION.md"       = "documentation\process\PR_DESCRIPTION.md";
    "PR_DESCRIPTION_TEMP.md"  = "documentation\process\PR_DESCRIPTION_TEMP.md";
    "PR_OCR_FEATURE.md"       = "documentation\process\PR_OCR_FEATURE.md";
    "BRANCH_STATUS.md"        = "documentation\process\BRANCH_STATUS.md";
    "COMMIT_SUMMARY.md"       = "documentation\process\COMMIT_SUMMARY.md";
    "MANIFEST.md"             = "documentation\process\MANIFEST.md";
    "WATCHDOG.md"             = "documentation\process\WATCHDOG.md";
    "WATCHDOG_SUMMARY.md"     = "documentation\process\WATCHDOG_SUMMARY.md";
    "GITHUB_SETUP_REVIEW.md"  = "documentation\process\GITHUB_SETUP_REVIEW.md";
}

foreach ($k in $map.Keys) {
    if (Test-Path (Join-Path $Root $k)) {
        GitMove $k $map[$k]
    }
}

# Move selected docs files into the new structure
$mapDocs = @{
    "docs\API_MODE_CONFIG.md"   = "documentation\api\API_MODE_CONFIG.md";
    "docs\OCR_QUICK_TEST.md"    = "documentation\ocr\OCR_QUICK_TEST.md";
    "docs\tailwind-v4-guide.md" = "documentation\guides\tailwind-v4-guide.md";
}
foreach ($k in $mapDocs.Keys) {
    if (Test-Path (Join-Path $Root $k)) {
        GitMove $k $mapDocs[$k]
    }
}

# Optional: update links in files to point to new locations for moved files
$pathMap = @{}
$map.GetEnumerator() | ForEach-Object { $pathMap[$_.Key] = $_.Value }
$mapDocs.GetEnumerator() | ForEach-Object { $pathMap[$_.Key] = $_.Value }

$targets = Get-ChildItem -Path $Root -Recurse -Include *.md,*.html | Where-Object { $_.FullName -notmatch "\\node_modules\\" }
foreach ($file in $targets) {
    $content = Get-Content $file.FullName -Raw
    $updated = $false
    foreach ($old in $pathMap.Keys) {
        $new = $pathMap[$old].Replace("documentation\", "documentation/").Replace("\", "/")
        $oldRel = $old.Replace("\", "/")
        if ($content -match [Regex]::Escape($oldRel)) {
            $content = $content -replace [Regex]::Escape($oldRel), $new
            $updated = $true
        }
    }
    if ($updated) {
        Set-Content -Path $file.FullName -Value $content
        & git add $file.FullName | Out-Null
        Write-Host "Updated links in: $($file.FullName)"
    }
}

Write-Host "Documentation organization complete."