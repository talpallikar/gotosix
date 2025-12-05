# GCP Cloud Run Deployment Guide

This guide walks you through deploying the MTG Mulligan Trainer to Google Cloud Platform using Cloud Run.

## Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Project with billing enabled
- MongoDB Atlas account (free tier available)

## Architecture

```
┌─────────────────┐
│   Cloud Build   │ ← GitHub/Git Push
└────────┬────────┘
         │
    ┌────▼────┐
    │ Artifact │
    │ Registry │
    └────┬────┘
         │
    ┌────▼─────────────────┐
    │    Cloud Run         │
    │  ┌──────────────┐    │
    │  │   Frontend   │    │
    │  │   (Nginx)    │    │
    │  └──────────────┘    │
    │  ┌──────────────┐    │
    │  │   Backend    │    │
    │  │   (Flask)    │    │
    │  └──────┬───────┘    │
    └─────────┼────────────┘
              │
    ┌─────────▼────────┐
    │ MongoDB Atlas    │
    │ (Managed DB)     │
    └──────────────────┘
```

## Step 1: Set Up GCP Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
export REGION="us-central1"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com
```

## Step 2: Create Artifact Registry Repository

```bash
# Create repository for Docker images
gcloud artifacts repositories create mtg-mulligan \
  --repository-format=docker \
  --location=$REGION \
  --description="MTG Mulligan Trainer container images"

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

## Step 3: Set Up MongoDB Atlas

1. **Create MongoDB Atlas Account:**
   - Go to https://www.mongodb.com/cloud/atlas
   - Sign up for free tier (512MB storage, perfect for starting)

2. **Create Cluster:**
   - Click "Build a Database"
   - Choose FREE tier (M0)
   - Select cloud provider: GCP
   - Region: us-central1 (Iowa) - same as Cloud Run
   - Cluster Name: mtg-mulligan

3. **Configure Network Access:**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Cloud Run uses dynamic IPs, so we need to allow all

4. **Create Database User:**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Username: `mtgapp`
   - Password: Generate strong password
   - Database User Privileges: "Read and write to any database"

5. **Get Connection String:**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Driver: Python, Version: 3.12+
   - Copy connection string:
   ```
   mongodb+srv://mtgapp:<password>@mtg-mulligan.xxxxx.mongodb.net/mtg_mulligan?retryWrites=true&w=majority
   ```
   - Replace `<password>` with your actual password

## Step 4: Store Secrets in Secret Manager

```bash
# Create secret for MongoDB URI
echo -n "mongodb+srv://mtgapp:YOUR_PASSWORD@mtg-mulligan.xxxxx.mongodb.net/mtg_mulligan?retryWrites=true&w=majority" | \
  gcloud secrets create mongodb-uri --data-file=-

# Create secret for Flask secret key
openssl rand -hex 32 | \
  gcloud secrets create app-secrets --data-file=-

# Grant Cloud Run access to secrets
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')

gcloud secrets add-iam-policy-binding mongodb-uri \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding app-secrets \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Step 5: Deploy Backend

```bash
# Build and push backend image
cd backend
gcloud builds submit \
  --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/backend:latest

# Deploy to Cloud Run
gcloud run deploy mtg-mulligan-backend \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/backend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars FLASK_ENV=production \
  --set-secrets MONGO_URI=mongodb-uri:latest,SECRET_KEY=app-secrets:latest \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 0

# Get backend URL
export BACKEND_URL=$(gcloud run services describe mtg-mulligan-backend \
  --region $REGION \
  --format 'value(status.url)')

echo "Backend URL: $BACKEND_URL"
```

## Step 6: Deploy Frontend

```bash
# Update frontend environment variable
cd ../frontend
echo "VITE_API_BASE_URL=$BACKEND_URL" > .env.production

# Build and push frontend image
gcloud builds submit \
  --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/frontend:latest

# Deploy to Cloud Run
gcloud run deploy mtg-mulligan-frontend \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/frontend:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 256Mi \
  --cpu 1 \
  --max-instances 10 \
  --min-instances 0

# Get frontend URL
export FRONTEND_URL=$(gcloud run services describe mtg-mulligan-frontend \
  --region $REGION \
  --format 'value(status.url)')

echo "Frontend URL: $FRONTEND_URL"
echo "Visit your app at: $FRONTEND_URL"
```

## Step 7: Set Up Continuous Deployment (Optional)

### Connect to GitHub

```bash
# Connect Cloud Build to GitHub
gcloud builds triggers create github \
  --name="mtg-mulligan-deploy" \
  --repo-name="mtg-mulligan-trainer" \
  --repo-owner="YOUR_GITHUB_USERNAME" \
  --branch-pattern="^main$" \
  --build-config="cloudbuild.yaml"
```

Now every push to `main` branch will automatically deploy!

## Costs

**Estimated Monthly Cost (Low Traffic):**
- Cloud Run: **FREE** (2M requests/month free)
- MongoDB Atlas: **FREE** (M0 tier, 512MB)
- Artifact Registry: **$0.10/month** (storage)
- Cloud Build: **FREE** (120 build-minutes/day)

**Total: ~$0-5/month** for hobbyist use

## Monitoring

### View Logs

```bash
# Backend logs
gcloud run services logs read mtg-mulligan-backend \
  --region $REGION \
  --limit 50

# Frontend logs
gcloud run services logs read mtg-mulligan-frontend \
  --region $REGION \
  --limit 50
```

### View Metrics

```bash
# Open Cloud Console
echo "Backend metrics: https://console.cloud.google.com/run/detail/$REGION/mtg-mulligan-backend/metrics"
echo "Frontend metrics: https://console.cloud.google.com/run/detail/$REGION/mtg-mulligan-frontend/metrics"
```

## Update Deployment

### Manual Update

```bash
# Rebuild and redeploy backend
cd backend
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/backend:latest
gcloud run deploy mtg-mulligan-backend \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/backend:latest \
  --region $REGION

# Rebuild and redeploy frontend
cd ../frontend
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/frontend:latest
gcloud run deploy mtg-mulligan-frontend \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/mtg-mulligan/frontend:latest \
  --region $REGION
```

### Automatic via Git

If you set up Cloud Build triggers, just push to main:

```bash
git add .
git commit -m "Update app"
git push origin main
# Cloud Build will automatically deploy!
```

## Environment Variables

### Backend
- `FLASK_ENV` - Set to `production`
- `MONGO_URI` - MongoDB connection string (from Secret Manager)
- `SECRET_KEY` - Flask secret key (from Secret Manager)
- `JWT_EXPIRATION_HOURS` - JWT token expiration (default: 24)

### Frontend
- `VITE_API_BASE_URL` - Backend Cloud Run URL

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
gcloud run services logs read mtg-mulligan-backend --region $REGION --limit 100

# Common issues:
# - MongoDB connection string incorrect
# - Secrets not accessible
# - Missing environment variables
```

### Frontend Can't Reach Backend

```bash
# Verify backend URL in frontend
gcloud run services describe mtg-mulligan-frontend --region $REGION

# Check VITE_API_BASE_URL is set correctly
# Rebuild frontend with correct backend URL
```

### CORS Errors

Flask-CORS is configured to allow all origins. If you see CORS errors:
- Check backend logs
- Verify backend is running
- Check browser console for actual error

## Custom Domain (Optional)

### Map Custom Domain

```bash
# Map domain to frontend
gcloud run domain-mappings create \
  --service mtg-mulligan-frontend \
  --domain yourdomain.com \
  --region $REGION

# Follow instructions to add DNS records
```

## Cleanup

To delete all resources:

```bash
# Delete Cloud Run services
gcloud run services delete mtg-mulligan-backend --region $REGION
gcloud run services delete mtg-mulligan-frontend --region $REGION

# Delete container images
gcloud artifacts repositories delete mtg-mulligan --location $REGION

# Delete secrets
gcloud secrets delete mongodb-uri
gcloud secrets delete app-secrets

# Delete MongoDB Atlas cluster (from Atlas console)
```

## Security Best Practices

1. ✅ **Use Secret Manager** for sensitive data
2. ✅ **Enable HTTPS** (automatic with Cloud Run)
3. ✅ **Restrict MongoDB access** to your IP or VPC (if possible)
4. ✅ **Rotate secrets** regularly
5. ✅ **Monitor logs** for suspicious activity
6. ✅ **Set up alerts** for errors/unusual traffic

## Next Steps

- Set up custom domain
- Configure Cloud CDN for better performance
- Add Cloud Armor for DDoS protection
- Set up Cloud Monitoring alerts
- Configure backup strategy for MongoDB

## Support

For issues:
- Cloud Run: https://cloud.google.com/run/docs
- MongoDB Atlas: https://docs.atlas.mongodb.com
- This app: https://github.com/YOUR_USERNAME/mtg-mulligan-trainer/issues
