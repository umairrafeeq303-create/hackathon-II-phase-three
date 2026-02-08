# Deployment Guide

This guide provides step-by-step instructions for deploying the Todo App to production.

## Project Structure

```
todo-app-phase-|||/
├── backend/          # FastAPI backend
├── frontend/         # Next.js frontend
└── DEPLOYMENT.md     # This file
```

## Prerequisites

- GitHub account with repository: https://github.com/umairrafeeq303-create/hackathon-II-phase-three
- Railway account: umairrafeeq303@gmail.com
- Vercel account (sign up with GitHub)
- Neon PostgreSQL database (already configured)

## Backend Deployment (Railway)

### Step 1: Push Code to GitHub (Already Done)
The code has been pushed to: https://github.com/umairrafeeq303-create/hackathon-II-phase-three

### Step 2: Deploy to Railway

1. Go to [Railway](https://railway.app/) and sign in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select: `umairrafeeq303-create/hackathon-II-phase-three`
4. Railway will auto-detect the Python app in `/backend`
5. Configure environment variables in Railway dashboard:

```env
DATABASE_URL=your_neon_database_url_from_env_example
BETTER_AUTH_SECRET=your_better_auth_secret_from_env_example
CORS_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
OPENAI_API_KEY=your_openai_api_key_from_env_example
PORT=8000
```

6. Railway will automatically:
   - Detect `Procfile` and `railway.json`
   - Install dependencies from `requirements.txt`
   - Run database migrations
   - Start the server with `uvicorn`

7. Once deployed, copy your Railway backend URL (e.g., `https://your-app.up.railway.app`)

### Step 3: Update CORS Origins

After deploying the frontend (next section), update the `CORS_ORIGINS` environment variable in Railway:
```
CORS_ORIGINS=https://your-frontend.vercel.app,https://your-frontend-*.vercel.app
```

## Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Go to [Vercel](https://vercel.com/) and sign in with GitHub
2. Click "Add New Project" → "Import Git Repository"
3. Select: `umairrafeeq303-create/hackathon-II-phase-three`
4. Configure project settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Add environment variables in Vercel:

```env
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
BETTER_AUTH_SECRET=your_better_auth_secret_from_env_example
```

6. Click "Deploy"
7. Vercel will automatically build and deploy your frontend

### Step 2: Update Backend CORS

1. Copy your Vercel deployment URL (e.g., `https://your-app.vercel.app`)
2. Go back to Railway dashboard
3. Update `CORS_ORIGINS` environment variable to include your Vercel URL
4. Redeploy the backend

## Environment Variables Summary

### Backend (Railway)
| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | PostgreSQL connection string | Neon database URL |
| `BETTER_AUTH_SECRET` | Shared secret | Must match frontend |
| `CORS_ORIGINS` | Vercel URL | Allowed origins |
| `ENVIRONMENT` | production | Environment mode |
| `OPENAI_API_KEY` | OpenAI API key | For AI features |
| `PORT` | 8000 | Server port |

### Frontend (Vercel)
| Variable | Value | Description |
|----------|-------|-------------|
| `NEXT_PUBLIC_API_URL` | Railway backend URL | Backend API endpoint |
| `BETTER_AUTH_SECRET` | Shared secret | Must match backend |

## Post-Deployment Verification

### 1. Check Backend Health
```bash
curl https://your-backend.up.railway.app/health
# Expected: {"status":"healthy"}
```

### 2. Check API Documentation
Visit: `https://your-backend.up.railway.app/docs`

### 3. Test Frontend
1. Visit your Vercel URL
2. Try signing up and logging in
3. Create, update, and delete tasks
4. Test AI chat features

## Troubleshooting

### Backend Issues

**Problem**: 500 Internal Server Error
- Check Railway logs: Dashboard → Deployments → Logs
- Verify all environment variables are set correctly
- Ensure DATABASE_URL is accessible

**Problem**: CORS errors
- Update `CORS_ORIGINS` to include your Vercel URL
- Include wildcard for preview deployments: `https://your-app-*.vercel.app`

### Frontend Issues

**Problem**: "Failed to fetch" errors
- Verify `NEXT_PUBLIC_API_URL` points to Railway backend
- Ensure Railway backend is running
- Check browser console for CORS errors

**Problem**: Authentication not working
- Ensure `BETTER_AUTH_SECRET` matches on both frontend and backend
- Check that the secret is exactly the same (case-sensitive)

## Continuous Deployment

Both Railway and Vercel are configured for automatic deployments:
- **Push to `main` branch** → Automatic production deployment
- **Push to other branches** → Preview deployments (Vercel only)

## Support

- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard
- GitHub Repository: https://github.com/umairrafeeq303-create/hackathon-II-phase-three

---

**Generated**: 2026-02-08
**Status**: Ready for deployment
