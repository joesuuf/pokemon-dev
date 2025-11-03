import os
import sys
import subprocess
from pathlib import Path

def ensure_dir(root: Path, rel_path: str):
    dest = root / rel_path
    dest.mkdir(parents=True, exist_ok=True)

def git_move(root: Path, src: str, dest: str):
    dest_parent = os.path.dirname(dest)
    if dest_parent:
        ensure_dir(root, dest_parent)
    print(f"Moving {src} -> {dest}")
    subprocess.run(["git", "mv", src, dest], cwd=root, check=True)

def main():
    root_arg = "c:\\claude-code\\pokemon-dev"
    if len(sys.argv) > 1:
        root_arg = sys.argv[1]
    root = Path(root_arg)

    # Create base directories
    base_dirs = [
        "documentation",
        "documentation\\audits\\collection",
        "documentation\\audits\\guides",
        "documentation\\guides",
        "documentation\\deployment",
        "documentation\\process",
        "documentation\\security",
        "documentation\\api",
        "documentation\\ocr",
    ]
    for d in base_dirs:
        ensure_dir(root, d)

    # Move entire audits directory -> consolidated audits collection
    if (root / "audits").exists():
        git_move(root, "audits", "documentation\\audits\\collection")

    # Move docs\\audits subfolders -> audits guides
    if (root / "docs" / "audits").exists():
        git_move(root, "docs\\audits", "documentation\\audits\\guides")

    # Map root-level markdown files to new locations
    mapping = {
        "API_KEYS_SETUP.md":       "documentation\\api\\API_KEYS_SETUP.md",
        "AUDIT_REPORT_REACT.md":   "documentation\\audits\\collection\\AUDIT_REPORT_REACT.md",
        "AUDIT_SUMMARY.md":        "documentation\\audits\\collection\\AUDIT_SUMMARY.md",
        "SCRIPT_AUDIT_REPORT.md":  "documentation\\audits\\collection\\SCRIPT_AUDIT_REPORT.md",

        "BUCKET_SECURITY.md":      "documentation\\security\\BUCKET_SECURITY.md",

        "DEPLOYMENT_SUMMARY.md":   "documentation\\deployment\\DEPLOYMENT_SUMMARY.md",
        "DEPLOY_NOW.md":           "documentation\\deployment\\DEPLOY_NOW.md",
        "GCP_DEPLOYMENT_READY.md": "documentation\\deployment\\GCP_DEPLOYMENT_READY.md",
        "GCP_VS_GITHUB_PAGES.md":  "documentation\\deployment\\GCP_VS_GITHUB_PAGES.md",
        "STATIC_SITE_EXPORT.md":   "documentation\\deployment\\STATIC_SITE_EXPORT.md",

        "GCP_SETUP_GUIDE.md":      "documentation\\guides\\GCP_SETUP_GUIDE.md",
        "WSL_SETUP.md":            "documentation\\guides\\WSL_SETUP.md",
        "WSL_DEV_RUNNER.md":       "documentation\\guides\\WSL_DEV_RUNNER.md",
        "DEV_PORTS_GUIDE.md":      "documentation\\guides\\DEV_PORTS_GUIDE.md",
        "FRONTEND_PORTS.md":       "documentation\\guides\\FRONTEND_PORTS.md",
        "DUAL_DEPLOYMENT_GUIDE.md":"documentation\\guides\\DUAL_DEPLOYMENT_GUIDE.md",
        "SETUP-BOTH-REPOS.md":     "documentation\\guides\\SETUP-BOTH-REPOS.md",
        "REMOTE_ACCESS.md":        "documentation\\guides\\REMOTE_ACCESS.md",

        "PR-DETAILS.md":           "documentation\\process\\PR-DETAILS.md",
        "PR_DESCRIPTION.md":       "documentation\\process\\PR_DESCRIPTION.md",
        "PR_DESCRIPTION_TEMP.md":  "documentation\\process\\PR_DESCRIPTION_TEMP.md",
        "PR_OCR_FEATURE.md":       "documentation\\process\\PR_OCR_FEATURE.md",
        "BRANCH_STATUS.md":        "documentation\\process\\BRANCH_STATUS.md",
        "COMMIT_SUMMARY.md":       "documentation\\process\\COMMIT_SUMMARY.md",
        "MANIFEST.md":             "documentation\\process\\MANIFEST.md",
        "WATCHDOG.md":             "documentation\\process\\WATCHDOG.md",
        "WATCHDOG_SUMMARY.md":     "documentation\\process\\WATCHDOG_SUMMARY.md",
        "GITHUB_SETUP_REVIEW.md":  "documentation\\process\\GITHUB_SETUP_REVIEW.md",
    }

    for k, dest in mapping.items():
        if (root / k).exists():
            git_move(root, k, dest)

    # Move selected docs files into the new structure
    map_docs = {
        "docs\\API_MODE_CONFIG.md":   "documentation\\api\\API_MODE_CONFIG.md",
        "docs\\OCR_QUICK_TEST.md":    "documentation\\ocr\\OCR_QUICK_TEST.md",
        "docs\\tailwind-v4-guide.md": "documentation\\guides\\tailwind-v4-guide.md",
    }
    for k, dest in map_docs.items():
        if (root / k).exists():
            git_move(root, k, dest)

    # Optional: update links in files to point to new locations for moved files
    path_map = {}
    path_map.update(mapping)
    path_map.update(map_docs)

    targets = []
    for dirpath, dirnames, filenames in os.walk(root):
        if "node_modules" in dirpath:
            continue
        for fn in filenames:
            if fn.lower().endswith(".md") or fn.lower().endswith(".html"):
                targets.append(Path(dirpath) / fn)

    for file_path in targets:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            # Skip unreadable files
            continue

        updated = False
        for old, new in path_map.items():
            new_norm = new.replace("documentation\\", "documentation/").replace("\\", "/")
            old_rel = old.replace("\\", "/")
            if old_rel in content:
                content = content.replace(old_rel, new_norm)
                updated = True

        if updated:
            file_path.write_text(content, encoding="utf-8", errors="ignore")
            subprocess.run(["git", "add", str(file_path)], cwd=root, check=False)
            print(f"Updated links in: {file_path}")

    print("Documentation organization complete.")

if __name__ == "__main__":
    main()