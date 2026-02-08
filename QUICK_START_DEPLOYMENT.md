# Quick Start Deployment Guide

Your code is now on GitHub! Follow these steps to deploy:

## GitHub Repository
✅ Successfully pushed to: https://github.com/umairrafeeq303-create/hackathon-II-phase-three

## Step 1: Deploy Backend to Railway (5 minutes)

### 1.1 Login to Railway
1. Go to https://railway.app/
2. Sign in with: **umairrafeeq303@gmail.com**

### 1.2 Create New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: `umairrafeeq303-create/hackathon-II-phase-three`
4. Railway will detect the Python app automatically

### 1.3 Configure Environment Variables
Click on your service → **Variables** → Add these:

```
DATABASE_URL=<copy from .env.production file>

BETTER_AUTH_SECRET=<copy from .env.production file>

CORS_ORIGINS=http://localhost:3001

ENVIRONMENT=production

OPENAI_API_KEY=<copy from .env.production file>

PORT=8000
```

### 1.4 Configure Root Directory
1. Go to **Settings** → **Root Directory**
2. Set to: `backend`
3. Click **Save**

### 1.5 Deploy
1. Railway will automatically start deploying
2. Wait 2-3 minutes for deployment to complete
3. Copy your Railway URL (e.g., `https://hackathon-ii-phase-three-production.up.railway.app`)

---

## Step 2: Deploy Frontend to Vercel (5 minutes)

### 2.1 Login to Vercel
1. Go to https://vercel.com/
2. Click **"Sign Up"** or **"Login"**
3. Choose **"Continue with GitHub"**

### 2.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Select: `umairrafeeq303-create/hackathon-II-phase-three`
3. Configure project settings:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `frontend` ← IMPORTANT!
   - **Build Command**: `npm run build` (auto-filled)
   - **Output Directory**: `.next` (auto-filled)

### 2.3 Add Environment Variables
Click **"Environment Variables"** and add:

```
NEXT_PUBLIC_API_URL=https://your-railway-url-from-step-1.up.railway.app

BETTER_AUTH_SECRET=<copy from .env.production file>
```

⚠️ Replace `your-railway-url-from-step-1.up.railway.app` with your actual Railway URL from Step 1.5

### 2.4 Deploy
1. Click **"Deploy"**
2. Wait 3-5 minutes for build and deployment
3. Copy your Vercel URL (e.g., `https://hackathon-ii-phase-three.vercel.app`)

---

## Step 3: Update CORS Settings (2 minutes)

Now that frontend is deployed, update backend CORS:

1. Go back to **Railway Dashboard**
2. Click on your backend service
3. Go to **Variables**
4. Update `CORS_ORIGINS` to:
```
CORS_ORIGINS=https://your-vercel-url.vercel.app,https://hackathon-ii-phase-three-*.vercel.app
```
5. Replace `your-vercel-url.vercel.app` with your actual Vercel URL
6. Railway will automatically redeploy with new settings

---

## Step 4: Test Your Deployment

### Test Backend
Visit: `https://your-railway-url.up.railway.app/health`

Expected response:
```json
{"status": "healthy"}
```

### Test API Documentation
Visit: `https://your-railway-url.up.railway.app/docs`

You should see FastAPI interactive documentation

### Test Frontend
1. Visit your Vercel URL
2. Click **"Sign Up"** and create an account
3. Login with your credentials
4. Try creating, editing, and deleting tasks
5. Test the AI chat feature

---

## URLs Summary

After deployment, save these URLs:

| Service | URL | Purpose |
|---------|-----|---------|
| GitHub | https://github.com/umairrafeeq303-create/hackathon-II-phase-three | Source code |
| Railway (Backend) | `https://your-app.up.railway.app` | API server |
| Vercel (Frontend) | `https://your-app.vercel.app` | Web interface |

---

## Automatic Deployments

Both platforms are configured for auto-deploy:

- **Push to `main`** → Automatic production deployment
- **Railway**: Monitors `backend/` directory
- **Vercel**: Monitors `frontend/` directory

---

## Troubleshooting

### Backend not deploying?
- Check Railway logs: Dashboard → Deployments → View Logs
- Verify all environment variables are set
- Ensure root directory is set to `backend`

### Frontend showing connection errors?
- Verify `NEXT_PUBLIC_API_URL` matches your Railway URL exactly
- Check that backend is running (visit `/health` endpoint)
- Look for CORS errors in browser console

### CORS errors?
- Ensure `CORS_ORIGINS` in Railway includes your Vercel URL
- Include preview deployments: `https://your-app-*.vercel.app`

---

## Support

All deployment configurations are already set up in:
- `backend/Procfile` - Railway startup command
- `backend/railway.json` - Railway configuration
- `frontend/vercel.json` - Vercel configuration
- `.env.production` - Reference for environment variables (DO NOT COMMIT)

For detailed information, see `DEPLOYMENT.md`

---

**Total Time**: ~15 minutes
**Status**: Ready to deploy! 🚀
