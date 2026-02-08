# Docker-Based Deployment Guide
## Railway (Backend) + Vercel (Frontend)

This guide fixes the "pip: command not found" and "start.sh not found" errors with a Docker-based approach.

---

## 🔧 Problem Fixed

**Previous Errors:**
- ❌ `/bin/bash: line 1: pip: command not found`
- ❌ `start.sh not found`
- ❌ Railway couldn't determine how to build

**Solution:**
- ✅ Created proper `Dockerfile` with Python 3.11 base image
- ✅ Configured Railway to use Docker builder
- ✅ All dependencies properly installed
- ✅ Multiple startup methods available

---

## 📁 Files Created

### Backend (Railway)
1. **`backend/Dockerfile`** - Main deployment file
   - Python 3.11 base image
   - Installs pip and all dependencies
   - Runs migrations automatically
   - Starts uvicorn server

2. **`backend/.dockerignore`** - Excludes unnecessary files from Docker build

3. **`backend/railway.json`** - Railway configuration (uses Dockerfile)

4. **`backend/start.sh`** - Alternative startup script (if needed)

---

## 🚀 Part 1: Railway Backend Deployment

### Step 1.1: Login to Railway

1. Go to: **https://railway.app/**
2. Click **"Login"**
3. Sign in with GitHub

### Step 1.2: Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose: `umairrafeeq303-create/hackathon-II-phase-three`
4. Railway will start analyzing your repository

### Step 1.3: Configure Service

1. Once created, click on your service
2. Go to **"Settings"** tab
3. Scroll to **"Root Directory"**
4. Enter: `backend`
5. Click **"Save"**

### Step 1.4: Verify Builder

Railway should automatically detect the Dockerfile. To verify:

1. Go to **"Settings"** → **"Builder"**
2. Should show: **"Dockerfile"**
3. If not, select **"Dockerfile"** from dropdown

### Step 1.5: Add Environment Variables

Click **"Variables"** tab and add these **7 variables**:

#### Variable 1: DATABASE_URL
```
postgresql://neondb_owner:npg_RXxtyQeP4d7l@ep-winter-pine-ahqb8d97-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

#### Variable 2: BETTER_AUTH_SECRET
```
XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo
```

#### Variable 3: CORS_ORIGINS
```
http://localhost:3001
```
(We'll update this after Vercel deployment)

#### Variable 4: ENVIRONMENT
```
production
```

#### Variable 5: OPENAI_API_KEY
```
Copy from your backend/.env file line 15
```

#### Variable 6: PORT
```
8000
```

#### Variable 7: PYTHONUNBUFFERED (Optional but recommended)
```
1
```

### Step 1.6: Deploy

1. Railway will automatically start deploying
2. Watch the build logs:
   - Building Docker image
   - Installing dependencies
   - Running migrations
   - Starting server

**Build time:** 3-5 minutes

### Step 1.7: Check Deployment Logs

Click on **"Deployments"** → Latest deployment → **"View Logs"**

You should see:
```
Starting FastAPI application...
Python version: 3.11.x
Running database migrations...
Starting uvicorn server...
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 1.8: Generate Domain

1. Go to **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy your Railway URL (e.g., `https://hackathon-ii-phase-three-production.up.railway.app`)

### Step 1.9: Test Backend

**Test 1: Health Check**
```bash
curl https://your-railway-url.up.railway.app/health
```

**Expected Response:**
```json
{"status":"healthy"}
```

**Test 2: API Documentation**

Open in browser:
```
https://your-railway-url.up.railway.app/docs
```

You should see the FastAPI Swagger UI.

---

## 📦 Part 2: Vercel Frontend Deployment

### Step 2.1: Login to Vercel

1. Go to: **https://vercel.com/**
2. Click **"Sign Up"** or **"Login"**
3. Choose **"Continue with GitHub"**

### Step 2.2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Find: `umairrafeeq303-create/hackathon-II-phase-three`
3. Click **"Import"**

### Step 2.3: Configure Project Settings

**IMPORTANT - Set these correctly:**

#### Framework Preset
- Should auto-detect: **Next.js**

#### Root Directory
- Click **"Edit"**
- Enter: `frontend`
- Click **"Continue"**

#### Build & Development Settings
- **Build Command:** `npm run build` (auto-filled)
- **Output Directory:** `.next` (auto-filled)
- **Install Command:** `npm install` (auto-filled)

### Step 2.4: Add Environment Variables

Expand **"Environment Variables"** section and add:

#### Variable 1: NEXT_PUBLIC_API_URL
```
Name: NEXT_PUBLIC_API_URL
Value: https://your-railway-url.up.railway.app
```
**Replace** `your-railway-url.up.railway.app` with your **actual Railway URL** from Step 1.8

#### Variable 2: BETTER_AUTH_SECRET
```
Name: BETTER_AUTH_SECRET
Value: XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo
```
**Must match** the backend secret exactly!

### Step 2.5: Deploy

1. Click **"Deploy"**
2. Vercel will:
   - Clone repository
   - Install dependencies
   - Build Next.js app
   - Deploy to CDN

**Build time:** 3-5 minutes

### Step 2.6: Monitor Build

Watch the build logs for:
- ✓ Installing dependencies
- ✓ Linting
- ✓ Type checking
- ✓ Building application
- ✓ Collecting page data
- ✓ Generating static pages
- ✓ Finalizing build

### Step 2.7: Get Vercel URL

Once deployed:
1. You'll see **"Congratulations!"**
2. Copy your Vercel URL (e.g., `https://hackathon-ii-phase-three.vercel.app`)
3. Click **"Visit"** to test

---

## 🔗 Part 3: Update CORS Configuration

Now that frontend is deployed, update backend CORS:

### Step 3.1: Update Railway CORS_ORIGINS

1. Go back to **Railway Dashboard**
2. Click on your backend service
3. Go to **"Variables"** tab
4. Find `CORS_ORIGINS`
5. Click **"Edit"** (pencil icon)
6. Update value to:

```
https://hackathon-ii-phase-three.vercel.app,https://hackathon-ii-phase-three-*.vercel.app
```

**Replace** `hackathon-ii-phase-three` with your actual Vercel project name.

7. Click **"Save"**

### Step 3.2: Wait for Redeploy

Railway will automatically redeploy with new CORS settings.

**Redeploy time:** 1-2 minutes

---

## ✅ Part 4: Complete Testing

### Test 1: Backend Health
```bash
curl https://your-railway-url.up.railway.app/health
```
**Expected:** `{"status":"healthy"}`

### Test 2: Backend API Docs
Open: `https://your-railway-url.up.railway.app/docs`

**Expected:** FastAPI Swagger UI

### Test 3: Frontend Homepage
Open: `https://your-vercel-url.vercel.app`

**Expected:** Landing page loads

### Test 4: User Signup
1. Click **"Sign Up"** or **"Get Started"**
2. Enter:
   - Email: `test@example.com`
   - Password: `TestPassword123`
3. Click **"Sign Up"**

**Expected:** Redirected to dashboard

### Test 5: User Login
1. Log out
2. Click **"Login"**
3. Enter credentials from Test 4
4. Click **"Login"**

**Expected:** Successfully logged in

### Test 6: Task Management
1. **Create:** Click "Add Task" → Enter title and description → Save
2. **Edit:** Click task → Edit → Save changes
3. **Complete:** Click checkbox to mark complete
4. **Delete:** Click delete icon → Confirm

**Expected:** All CRUD operations work

### Test 7: AI Chat Feature
1. Navigate to Chat page or click AI assistant icon
2. Type: `"Show me all my tasks"`
3. AI should respond with your task list
4. Try: `"Create a task to buy groceries"`

**Expected:** AI creates the task

---

## 🐛 Troubleshooting

### Problem: "pip: command not found" during build

**Solution:** ✅ Already fixed! The Dockerfile uses `python:3.11-slim` which includes pip.

If you still see this:
1. Check that `railway.json` has `"builder": "DOCKERFILE"`
2. Verify Dockerfile exists in `backend/` directory
3. Redeploy: **Deployments** → **"Redeploy"**

### Problem: "start.sh not found"

**Solution:** ✅ Not needed! Docker uses the `CMD` instruction in Dockerfile.

The start command is:
```dockerfile
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

### Problem: Database connection errors

**Solutions:**
1. Verify `DATABASE_URL` is correct in Railway variables
2. Check Neon database is active
3. Check Railway logs for connection errors
4. Test connection: `psql $DATABASE_URL -c "SELECT 1"`

### Problem: Frontend shows "Failed to fetch"

**Solutions:**
1. Check `NEXT_PUBLIC_API_URL` matches Railway URL exactly
2. Must use `https://` not `http://`
3. No trailing slash in URL
4. Redeploy Vercel after changing environment variable

### Problem: CORS errors

**Symptoms:**
- Browser console shows CORS error
- API requests fail from frontend

**Solutions:**
1. Verify `CORS_ORIGINS` in Railway includes Vercel URL
2. Must use `https://` protocol
3. Include preview deployments: `https://your-app-*.vercel.app`
4. Wait 1-2 minutes for Railway to redeploy

### Problem: 500 Internal Server Error

**Debug Steps:**
1. Check Railway logs: **Deployments** → **View Logs**
2. Common causes:
   - Missing environment variable
   - Database connection failed
   - Import error in code
3. Check specific error in logs
4. Fix and redeploy

### Problem: Build fails with "requirements.txt not found"

**Solution:**
1. Check that Root Directory is set to `backend`
2. Verify `requirements.txt` exists in backend directory
3. Check `.dockerignore` doesn't exclude it

### Problem: Authentication not working

**Solutions:**
1. Ensure `BETTER_AUTH_SECRET` is **exactly** the same on both Railway and Vercel
2. Case-sensitive comparison
3. No extra spaces or quotes
4. Redeploy both if changed

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Railway account ready
- [ ] GitHub account connected
- [ ] Vercel account created
- [ ] Environment variables documented
- [ ] Dockerfile reviewed

### Railway Backend
- [ ] Service created from GitHub repo
- [ ] Root directory set to `backend`
- [ ] Builder set to "Dockerfile"
- [ ] All 7 environment variables added
- [ ] Deployment successful (no errors in logs)
- [ ] Health endpoint works: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Railway URL copied

### Vercel Frontend
- [ ] Project imported from GitHub
- [ ] Root directory set to `frontend`
- [ ] Framework preset: Next.js
- [ ] Environment variables added (2)
- [ ] Build successful (no errors)
- [ ] Homepage loads
- [ ] Vercel URL copied

### Integration
- [ ] CORS_ORIGINS updated in Railway
- [ ] No CORS errors in browser console
- [ ] Can sign up new user
- [ ] Can login
- [ ] Can create task
- [ ] Can edit task
- [ ] Can delete task
- [ ] AI chat responds

---

## 🎯 Environment Variables Summary

### Railway (Backend) - 7 Required
| Variable | Value | Notes |
|----------|-------|-------|
| `DATABASE_URL` | Neon PostgreSQL connection string | From .env.production |
| `BETTER_AUTH_SECRET` | XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo | Must match frontend |
| `CORS_ORIGINS` | https://your-vercel-url.vercel.app,... | Update after Vercel deploy |
| `ENVIRONMENT` | production | Static value |
| `OPENAI_API_KEY` | sk-proj-... | From backend/.env line 15 |
| `PORT` | 8000 | Railway overrides automatically |
| `PYTHONUNBUFFERED` | 1 | Optional, for better logs |

### Vercel (Frontend) - 2 Required
| Variable | Value | Notes |
|----------|-------|-------|
| `NEXT_PUBLIC_API_URL` | https://your-railway-url.up.railway.app | From Railway deployment |
| `BETTER_AUTH_SECRET` | XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo | Must match backend |

---

## 🔄 Continuous Deployment

### Auto-Deploy on Push
Both platforms auto-deploy when you push to GitHub:

**Railway:**
- Watches: `backend/` directory
- Trigger: Push to `main` branch
- Build time: ~3-4 minutes
- Uses: Dockerfile

**Vercel:**
- Watches: `frontend/` directory
- Trigger: Push to any branch
- Main branch → Production
- Other branches → Preview
- Build time: ~3-5 minutes

---

## 📂 File Structure

```
backend/
├── Dockerfile              ← NEW: Main deployment file
├── .dockerignore          ← NEW: Docker ignore file
├── railway.json           ← UPDATED: Uses Dockerfile
├── start.sh               ← UPDATED: Alternative startup
├── Procfile               ← Fallback method
├── requirements.txt       ← Dependencies
├── runtime.txt            ← Python version
├── alembic.ini            ← Migration config
├── src/
│   ├── main.py           ← FastAPI app entry
│   ├── api/              ← API routes
│   ├── core/             ← Config, security
│   ├── db/               ← Database
│   └── models/           ← SQLModel models
└── alembic/              ← Migrations

frontend/
├── vercel.json           ← Vercel config
├── package.json          ← Dependencies
├── next.config.js        ← Next.js config
└── src/
    ├── app/              ← Next.js 14 app router
    ├── components/       ← React components
    └── lib/              ← API client, utils
```

---

## 🎓 Understanding the Dockerfile

```dockerfile
FROM python:3.11-slim                    # ← Base image with Python & pip
WORKDIR /app                              # ← Set working directory
ENV PYTHONUNBUFFERED=1                    # ← Real-time logs
RUN apt-get install gcc postgresql-client # ← System dependencies
COPY requirements.txt .                   # ← Copy dependency list
RUN pip install -r requirements.txt       # ← Install Python packages
COPY . .                                  # ← Copy application code
EXPOSE 8000                               # ← Document port
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

Key features:
- ✅ Python 3.11 with pip included
- ✅ Automatic database migrations
- ✅ Non-root user for security
- ✅ Health check configured
- ✅ Optimized layer caching

---

## 📞 Support Resources

- **Railway Docs:** https://docs.railway.app/
- **Vercel Docs:** https://vercel.com/docs
- **Docker Docs:** https://docs.docker.com/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Next.js Docs:** https://nextjs.org/docs

---

## ✨ What's Different from Previous Attempts

### Before (Nixpacks/Buildpacks):
- ❌ "pip: command not found"
- ❌ "start.sh not found"
- ❌ Inconsistent builds
- ❌ Railway couldn't determine builder

### Now (Docker):
- ✅ Explicit Python 3.11 base image
- ✅ pip always available
- ✅ Start command in Dockerfile
- ✅ Consistent, reproducible builds
- ✅ Works on any platform

---

## 🚀 Ready to Deploy!

**Total Time:** ~15 minutes
- Railway: 5 minutes
- Vercel: 5 minutes
- CORS Update: 2 minutes
- Testing: 3 minutes

**Next Step:** Follow Part 1 to deploy backend to Railway

Good luck! 🎉
