# Create standard audit categories
mkdir -p audits/general
mkdir -p audits/security
mkdir -p audits/performance
mkdir -p audits/workflow
mkdir -p audits/testing
mkdir -p audits/seo

# Create new documentation categories
mkdir -p docs/setup
mkdir -p docs/deployment
mkdir -p docs/features
mkdir -p docs/project
mkdir -p docs/guides

# Move Security Audits
mv BUCKET_SECURITY.md audits/security/
mv SECURITY-AUDIT-COMPREHENSIVE.md audits/security/
mv SECURITY-AUDIT-SUMMARY.md audits/security/
mv SECURITY-QUICK-REFERENCE.md audits/security/
mv SECURITY-REMEDIATION-PLAN.md audits/security/
mv SECURITY_AGENT_V2_MIGRATION.md audits/security/
mv SECURITY_ENHANCEMENTS_SUMMARY.md audits/security/

# Move Performance Audits
mv AUDIT_REPORT_REACT.md audits/performance/
mv AUDIT_REPORT_STATIC_SITE.md audits/performance/

# Move Workflow/Script Audits
mv SCRIPT_AUDIT_REPORT.md audits/workflow/
mv WORKFLOW_AUDIT_REPORT.md audits/workflow/

# Move Testing Audits
mv STANDALONE_VERIFICATION.md audits/testing/

# Move General Audits
mv AUDIT_SUMMARY.md audits/general/

# Move Setup Guides
mv API_KEYS_SETUP.md docs/setup/
mv GCP_SETUP_GUIDE.md docs/setup/
mv GITHUB_SETUP_REVIEW.md docs/setup/
mv SETUP-BOTH-REPOS.md docs/setup/
mv WSL_DEV_RUNNER.md docs/setup/
mv WSL_SETUP.md docs/setup/

# Move Deployment Docs
mv DEPLOYMENT_SUMMARY.md docs/deployment/
mv DEPLOY_NOW.md docs/deployment/
mv DUAL_DEPLOYMENT_GUIDE.md docs/deployment/
mv GCP_DEPLOYMENT_READY.md docs/deployment/
mv GCP_VS_GITHUB_PAGES.md docs/deployment/
mv GITHUB_ACTIONS_SETTINGS.md docs/deployment/
mv GITHUB_PAGES_DEPLOYMENT.md docs/deployment/
mv GITHUB_PAGES_SETUP_SUMMARY.md docs/deployment/
mv STATIC_SITE_EXPORT.md docs/deployment/

# Move Project Management Docs
mv BRANCH_STATUS.md docs/project/
mv COMMIT_SUMMARY.md docs/project/
mv IMPLEMENTATION_COMPLETE.md docs/project/
mv MANIFEST.md docs/project/
mv MIGRATION_SUMMARY_2025-11-02.md docs/project/
mv PR-DETAILS.md docs/project/
mv PR_DESCRIPTION.md docs/project/
mv PR_DESCRIPTION_TEMP.md docs/project/
mv PR_TITLE.txt docs/project/
mv PR_TITLE_AND_SUMMARY.txt docs/project/

# Move Feature Docs
mv HTTP_SERVER_CAPABILITIES_TODO.md docs/features/
mv PR_OCR_FEATURE.md docs/features/

# Move General Guides
mv DEV_PORTS_GUIDE.md docs/guides/
mv FRONTEND_PORTS.md docs/guides/
mv IMAGE_DOWNLOADER_QUICKSTART.md docs/guides/
mv REMOTE_ACCESS.md docs/guides/
mv SERVICE_WORKER_ERROR_FIX.md docs/guides/
mv WATCHDOG.md docs/guides/
mv WATCHDOG_SUMMARY.md docs/guides/

# Move OCR feature docs into the new features folder
mv docs/OCR_*.md docs/features/

# Move files from the messy 'docs/audits' folder into the main '/audits' folder
mv docs/audits/performance/* audits/performance/
mv docs/audits/security/* audits/security/
mv docs/audits/seo/* audits/seo/
mv docs/audits/testing/* audits/testing/
mv docs/audits/*.md audits/general/
mv docs/audits/*.ipynb audits/general/

# Correct case-sensitivity issue (audits/SEO -> audits/seo)
mv audits/SEO/* audits/seo/

# Clean up now-empty legacy directories
rmdir docs/audits/performance
rmdir docs/audits/security
rmdir docs/audits/seo
rmdir docs/audits/testing
rmdir docs/audits
rmdir audits/SEO
