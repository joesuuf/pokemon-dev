#!/bin/bash

# ========================================================================
# Google Cloud Platform (GCP) Deployment Script
# ========================================================================
# Deploy Pokemon TCG Search to GCP with multiple deployment options:
# 1. Cloud Storage + Cloud CDN (Best for static sites)
# 2. Cloud Run (Best for containerized apps)
# 3. App Engine (Best for managed apps)
# ========================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "========================================================================"
echo "   Google Cloud Platform (GCP) Deployment"
echo "========================================================================"
echo -e "${NC}"

# Configuration
PROJECT_ID=""
BUCKET_NAME=""
REGION="us-central1"
BUILD_DIR="dist"
STATIC_SITE_DIR="static-site"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo ""
    echo "Install Google Cloud SDK:"
    echo "  https://cloud.google.com/sdk/docs/install"
    echo ""
    echo "Quick install (Linux/Mac):"
    echo "  curl https://sdk.cloud.google.com | bash"
    echo "  exec -l \$SHELL"
    echo "  gcloud init"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI is installed${NC}"
echo ""

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}You are not authenticated with gcloud${NC}"
    echo "Running: gcloud auth login"
    gcloud auth login
fi

ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)")
echo -e "${GREEN}✓ Authenticated as: $ACTIVE_ACCOUNT${NC}"
echo ""

# Get or select project
echo -e "${CYAN}Select or create a GCP project:${NC}"
echo ""

# List existing projects
echo "Existing projects:"
gcloud projects list --format="table(projectId,name,projectNumber)" 2>/dev/null || echo "No projects found"
echo ""

read -p "Enter project ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo ""
    read -p "Enter new project ID (lowercase, numbers, hyphens): " NEW_PROJECT_ID
    read -p "Enter project name: " PROJECT_NAME

    echo "Creating project: $NEW_PROJECT_ID"
    gcloud projects create "$NEW_PROJECT_ID" --name="$PROJECT_NAME"
    PROJECT_ID="$NEW_PROJECT_ID"

    echo -e "${GREEN}✓ Project created${NC}"
    echo ""
    echo -e "${YELLOW}⚠️  You need to enable billing for this project${NC}"
    echo "Visit: https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
    echo ""
    read -p "Press Enter after enabling billing..."
fi

# Set active project
gcloud config set project "$PROJECT_ID"
echo -e "${GREEN}✓ Active project: $PROJECT_ID${NC}"
echo ""

# Choose frontend version
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Which frontend do you want to deploy?${NC}"
echo ""
echo "  1) React Frontend (main React app)"
echo "     • ~150KB bundle (gzipped: ~50KB)"
echo "     • Requires build process"
echo "     • Best for: Complex applications"
echo ""
echo "  2) Static Site (recommended - 15x smaller, 30x faster)"
echo "     • ~10KB total"
echo "     • No build process"
echo "     • Best for: Maximum performance"
echo ""
echo "  3) Cancel"
echo ""

read -p "Enter your choice (1, 2, or 3): " FRONTEND_CHOICE

case $FRONTEND_CHOICE in
    1)
        FRONTEND_TYPE="react"
        echo -e "${BLUE}→ Selected: React Frontend${NC}"
        ;;
    2)
        FRONTEND_TYPE="static"
        echo -e "${BLUE}→ Selected: Static Site${NC}"
        ;;
    3)
        echo -e "${YELLOW}Deployment cancelled.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"

# Choose deployment method
echo -e "${GREEN}Choose GCP deployment method:${NC}"
echo ""
echo "  1) Cloud Storage + Cloud CDN (RECOMMENDED for static sites)"
echo "     • Best performance"
echo "     • Lowest cost (~\$0.01-\$0.50/month)"
echo "     • Global CDN"
echo "     • Custom domain support"
echo "     • 99.95% SLA"
echo ""
echo "  2) Cloud Run (Containerized deployment)"
echo "     • Auto-scaling"
echo "     • Pay per request"
echo "     • ~\$5-\$20/month (depends on traffic)"
echo "     • Serverless"
echo ""
echo "  3) App Engine (Managed platform)"
echo "     • Fully managed"
echo "     • Auto-scaling"
echo "     • ~\$10-\$50/month"
echo "     • More features"
echo ""
echo "  4) Cancel"
echo ""

read -p "Enter your choice (1-4): " DEPLOY_METHOD

case $DEPLOY_METHOD in
    1)
        DEPLOYMENT_TYPE="storage"
        echo -e "${BLUE}→ Selected: Cloud Storage + Cloud CDN${NC}"
        ;;
    2)
        DEPLOYMENT_TYPE="cloudrun"
        echo -e "${BLUE}→ Selected: Cloud Run${NC}"
        ;;
    3)
        DEPLOYMENT_TYPE="appengine"
        echo -e "${BLUE}→ Selected: App Engine${NC}"
        ;;
    4)
        echo -e "${YELLOW}Deployment cancelled.${NC}"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"

# Prepare deployment files
DEPLOY_DIR="gcp-deploy-temp"

echo ""
echo -e "${BLUE}Preparing deployment files...${NC}"

# Clean up old deployment directory
if [ -d "$DEPLOY_DIR" ]; then
    rm -rf "$DEPLOY_DIR"
fi

mkdir -p "$DEPLOY_DIR"

# Build or copy files based on frontend selection
if [ "$FRONTEND_TYPE" == "react" ]; then
    echo ""
    echo -e "${BLUE}Building React application...${NC}"

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}→ Running npm install...${NC}"
        npm install
    fi

    # Build React app
    echo "  → Building with Vite..."
    npm run build

    if [ ! -d "$BUILD_DIR" ]; then
        echo -e "${RED}Error: Build failed. $BUILD_DIR directory not found.${NC}"
        exit 1
    fi

    # Copy built files
    echo "  → Copying built files..."
    cp -r "$BUILD_DIR"/* "$DEPLOY_DIR/"

else  # static site
    echo ""
    echo -e "${BLUE}Preparing static site...${NC}"

    if [ ! -d "$STATIC_SITE_DIR" ]; then
        echo -e "${RED}Error: Static site directory not found${NC}"
        exit 1
    fi

    # Copy static site files
    echo "  → Copying static site files..."
    cp "$STATIC_SITE_DIR/index.html" "$DEPLOY_DIR/"
    cp -r "$STATIC_SITE_DIR/scripts" "$DEPLOY_DIR/"
    cp -r "$STATIC_SITE_DIR/styles" "$DEPLOY_DIR/"

    if [ -d "$STATIC_SITE_DIR/assets" ]; then
        cp -r "$STATIC_SITE_DIR/assets" "$DEPLOY_DIR/"
    fi
fi

echo -e "${GREEN}  ✓ Files prepared${NC}"

# Deploy based on selected method
case $DEPLOYMENT_TYPE in
    storage)
        echo ""
        echo -e "${BLUE}Deploying to Cloud Storage + Cloud CDN...${NC}"
        echo ""

        # Generate bucket name
        BUCKET_NAME="${PROJECT_ID}-pokemon-tcg"

        echo "Bucket name: $BUCKET_NAME"
        echo ""

        # Enable required APIs
        echo "  → Enabling Cloud Storage API..."
        gcloud services enable storage-api.googleapis.com --project="$PROJECT_ID" 2>/dev/null || true

        echo "  → Enabling Compute Engine API (for Cloud CDN)..."
        gcloud services enable compute.googleapis.com --project="$PROJECT_ID" 2>/dev/null || true

        # Create bucket
        echo "  → Creating storage bucket..."
        gsutil mb -p "$PROJECT_ID" -c STANDARD -l "$REGION" "gs://$BUCKET_NAME" 2>/dev/null || echo "    (bucket may already exist)"

        # Set bucket to public read
        echo "  → Making bucket publicly readable..."
        gsutil iam ch allUsers:objectViewer "gs://$BUCKET_NAME"

        # Enable website configuration
        echo "  → Configuring bucket for static website..."
        gsutil web set -m index.html -e index.html "gs://$BUCKET_NAME"

        # Upload files
        echo "  → Uploading files to bucket..."
        gsutil -m rsync -r -d "$DEPLOY_DIR" "gs://$BUCKET_NAME"

        # Set cache control
        echo "  → Setting cache control headers..."
        gsutil -m setmeta -h "Cache-Control:public, max-age=3600" "gs://$BUCKET_NAME/**"

        # Get bucket URL
        BUCKET_URL="https://storage.googleapis.com/$BUCKET_NAME/index.html"

        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}           DEPLOYMENT COMPLETE - CLOUD STORAGE                  ${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${CYAN}Deployment Information:${NC}"
        echo "  • Bucket: $BUCKET_NAME"
        echo "  • Project: $PROJECT_ID"
        echo "  • Region: $REGION"
        echo "  • Frontend: $FRONTEND_TYPE"
        echo ""
        echo -e "${CYAN}Access URLs:${NC}"
        echo "  • Storage URL: $BUCKET_URL"
        echo "  • Alternative: https://$BUCKET_NAME.storage.googleapis.com/index.html"
        echo ""

        # Cloud CDN setup instructions
        echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}              OPTIONAL: ENABLE CLOUD CDN                        ${NC}"
        echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "For better performance, enable Cloud CDN:"
        echo ""
        echo "1. Create a load balancer:"
        echo "   https://console.cloud.google.com/net-services/loadbalancing/list"
        echo ""
        echo "2. Backend configuration:"
        echo "   • Backend type: Cloud Storage bucket"
        echo "   • Bucket: $BUCKET_NAME"
        echo "   • Enable Cloud CDN: Yes"
        echo ""
        echo "3. Frontend configuration:"
        echo "   • Protocol: HTTPS"
        echo "   • IP: Create new IP address"
        echo ""
        echo "4. Create managed SSL certificate (optional)"
        echo ""
        ;;

    cloudrun)
        echo ""
        echo -e "${BLUE}Deploying to Cloud Run...${NC}"
        echo ""

        # Enable required APIs
        echo "  → Enabling Cloud Run API..."
        gcloud services enable run.googleapis.com --project="$PROJECT_ID"

        echo "  → Enabling Container Registry API..."
        gcloud services enable containerregistry.googleapis.com --project="$PROJECT_ID"

        # Create Dockerfile if it doesn't exist
        if [ ! -f "$DEPLOY_DIR/Dockerfile" ]; then
            echo "  → Creating Dockerfile..."
            cat > "$DEPLOY_DIR/Dockerfile" << 'EOF'
FROM nginx:alpine

# Copy static files
COPY . /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 (Cloud Run requirement)
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
EOF

            # Create nginx config
            cat > "$DEPLOY_DIR/nginx.conf" << 'EOF'
server {
    listen 8080;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Cache static assets
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
EOF
        fi

        SERVICE_NAME="pokemon-tcg-search"

        # Build and deploy
        echo "  → Building and deploying to Cloud Run..."
        gcloud run deploy "$SERVICE_NAME" \
            --source "$DEPLOY_DIR" \
            --platform managed \
            --region "$REGION" \
            --allow-unauthenticated \
            --project="$PROJECT_ID"

        # Get service URL
        SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)" --project="$PROJECT_ID")

        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}              DEPLOYMENT COMPLETE - CLOUD RUN                    ${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${CYAN}Deployment Information:${NC}"
        echo "  • Service: $SERVICE_NAME"
        echo "  • Project: $PROJECT_ID"
        echo "  • Region: $REGION"
        echo "  • URL: $SERVICE_URL"
        echo ""
        ;;

    appengine)
        echo ""
        echo -e "${BLUE}Deploying to App Engine...${NC}"
        echo ""

        # Enable App Engine API
        echo "  → Enabling App Engine API..."
        gcloud services enable appengine.googleapis.com --project="$PROJECT_ID"

        # Check if App Engine app exists
        if ! gcloud app describe --project="$PROJECT_ID" &>/dev/null; then
            echo "  → Creating App Engine application..."
            gcloud app create --region="$REGION" --project="$PROJECT_ID"
        fi

        # Create app.yaml
        echo "  → Creating app.yaml..."
        cat > "$DEPLOY_DIR/app.yaml" << 'EOF'
runtime: python39

handlers:
# Serve all static files
- url: /(.*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot))
  static_files: \1
  upload: .*\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)
  secure: always

# Serve index.html for root
- url: /
  static_files: index.html
  upload: index.html
  secure: always

# Serve index.html for all other routes (SPA)
- url: /.*
  static_files: index.html
  upload: index.html
  secure: always
EOF

        # Deploy
        echo "  → Deploying to App Engine..."
        gcloud app deploy "$DEPLOY_DIR/app.yaml" --project="$PROJECT_ID" --quiet

        # Get service URL
        APP_URL="https://${PROJECT_ID}.appspot.com"

        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}             DEPLOYMENT COMPLETE - APP ENGINE                    ${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${CYAN}Deployment Information:${NC}"
        echo "  • Project: $PROJECT_ID"
        echo "  • Region: $REGION"
        echo "  • URL: $APP_URL"
        echo ""
        ;;
esac

# Custom domain setup
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                  CUSTOM DOMAIN SETUP                            ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
read -p "Do you want to set up a custom domain? (y/n): " SETUP_DOMAIN

if [[ "$SETUP_DOMAIN" =~ ^[Yy]$ ]]; then
    read -p "Enter your custom domain: " CUSTOM_DOMAIN

    echo ""
    echo -e "${CYAN}Custom Domain Setup Instructions:${NC}"
    echo ""

    case $DEPLOYMENT_TYPE in
        storage)
            echo "1. Verify domain ownership in Google Search Console"
            echo "   https://search.google.com/search-console"
            echo ""
            echo "2. Create a load balancer with your bucket as backend"
            echo "   https://console.cloud.google.com/net-services/loadbalancing"
            echo ""
            echo "3. In Cloudflare DNS, add A record:"
            echo "   Type: A"
            echo "   Name: @ (or subdomain)"
            echo "   IPv4: [Load balancer IP]"
            echo "   Proxy: DNS only (gray cloud) or Proxied (orange cloud)"
            echo ""
            ;;
        cloudrun)
            echo "1. Map custom domain in Cloud Run:"
            echo "   gcloud run domain-mappings create --service=$SERVICE_NAME --domain=$CUSTOM_DOMAIN --region=$REGION"
            echo ""
            echo "2. Add DNS records in Cloudflare:"
            echo "   (gcloud will show required records after mapping)"
            echo ""
            ;;
        appengine)
            echo "1. Add custom domain in App Engine:"
            echo "   https://console.cloud.google.com/appengine/settings/domains"
            echo ""
            echo "2. Follow verification steps"
            echo ""
            echo "3. Add DNS records in Cloudflare as instructed"
            echo ""
            ;;
    esac
fi

# Cost estimation
echo ""
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                    COST ESTIMATION                              ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""

case $DEPLOYMENT_TYPE in
    storage)
        echo -e "${CYAN}Cloud Storage + CDN (estimated monthly):${NC}"
        echo "  • Storage (1GB): ~\$0.02/month"
        echo "  • Network egress (10GB): ~\$0.12/month"
        echo "  • Cloud CDN (optional): ~\$0.08/GB"
        echo "  • Total: ~\$0.15 - \$1.00/month"
        echo ""
        echo -e "${GREEN}→ CHEAPEST OPTION${NC}"
        ;;
    cloudrun)
        echo -e "${CYAN}Cloud Run (estimated monthly):${NC}"
        echo "  • CPU (pay per use): ~\$0.10/100K requests"
        echo "  • Memory: ~\$0.08/100K requests"
        echo "  • Network egress: ~\$0.12/GB"
        echo "  • Total: ~\$5 - \$20/month (typical)"
        echo ""
        echo -e "${YELLOW}→ MODERATE COST (scales with traffic)${NC}"
        ;;
    appengine)
        echo -e "${CYAN}App Engine (estimated monthly):${NC}"
        echo "  • Standard environment: ~\$0.05/hour"
        echo "  • Network egress: ~\$0.12/GB"
        echo "  • Total: ~\$10 - \$50/month"
        echo ""
        echo -e "${YELLOW}→ HIGHER COST (always running)${NC}"
        ;;
esac

echo ""
echo -e "${CYAN}GitHub Pages for comparison: \$0/month (free)${NC}"
echo ""

# Monitoring setup
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}                    MONITORING SETUP                             ${NC}"
echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Enable monitoring in GCP Console:"
echo "  • Cloud Monitoring: https://console.cloud.google.com/monitoring"
echo "  • Cloud Logging: https://console.cloud.google.com/logs"
echo ""

# Clean up
echo "  → Cleaning up temporary files..."
rm -rf "$DEPLOY_DIR"

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                    DEPLOYMENT COMPLETE!                          ${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}Next Steps:${NC}"
echo "1. Test your deployment"
echo "2. Set up custom domain (if desired)"
echo "3. Enable monitoring"
echo "4. Compare performance with GitHub Pages"
echo ""
echo -e "${CYAN}Useful Commands:${NC}"

case $DEPLOYMENT_TYPE in
    storage)
        echo "  • View bucket: gsutil ls gs://$BUCKET_NAME"
        echo "  • Update files: gsutil -m rsync -r -d [local-dir] gs://$BUCKET_NAME"
        echo "  • Delete bucket: gsutil rm -r gs://$BUCKET_NAME"
        ;;
    cloudrun)
        echo "  • View service: gcloud run services describe $SERVICE_NAME --region=$REGION"
        echo "  • Update: gcloud run deploy $SERVICE_NAME --source . --region=$REGION"
        echo "  • Delete: gcloud run services delete $SERVICE_NAME --region=$REGION"
        ;;
    appengine)
        echo "  • View app: gcloud app browse"
        echo "  • View logs: gcloud app logs tail"
        echo "  • Versions: gcloud app versions list"
        ;;
esac

echo ""
echo -e "${GREEN}GCP deployment completed successfully!${NC}"
echo ""
