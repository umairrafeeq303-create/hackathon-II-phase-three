# Railway + Vercel Deployment Guide

Complete step-by-step guide to deploy your FastAPI + Next.js application.

---

## 🚂 Part 1: Railway Backend Deployment

### Step 1.1: Create New Railway Project

1. Go to https://railway.app/
2. Click **"Login"** and sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose: `umairrafeeq303-create/hackathon-II-phase-three`

### Step 1.2: Configure Service Settings

After Railway creates the project:

1. Click on your service (should auto-detect Python)
2. Go to **"Settings"** tab
3. Scroll to **"Root Directory"**
4. Set to: `backend`
5. Click **"Save"**

### Step 1.3: Add Environment Variables

1. Click on **"Variables"** tab
2. Click **"+ New Variable"** and add each of these:

```bash
# Database URL (from your .env.production)
DATABASE_URL
postgresql://neondb_owner:npg_RXxtyQeP4d7l@ep-winter-pine-ahqb8d97-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require

# Authentication Secret (from your .env.production)
BETTER_AUTH_SECRET
XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo

# CORS Origins (we'll update this after Vercel deployment)
CORS_ORIGINS
http://localhost:3001

# Environment
ENVIRONMENT
production

# OpenAI API Key (copy from your .env.production or backend/.env file)
OPENAI_API_KEY
sk-proj-your_openai_api_key_here

# Port (Railway will auto-assign, but we set default)
PORT
8000
```

**Pro Tip:** Copy-paste each variable name and value separately to avoid errors.

### Step 1.4: Trigger Deployment

1. Go to **"Deployments"** tab
2. Railway should start deploying automatically
3. If not, click **"Deploy"** button
4. Wait 3-5 minutes for build and deployment

### Step 1.5: Monitor Deployment

Watch the deployment logs:
1. Click on the latest deployment
2. You should see:
   - `Installing dependencies...`
   - `pip install -r requirements.txt`
   - `Starting application...`
   - `uvicorn src.main:app...`

### Step 1.6: Get Your Railway URL

1. Once deployed, go to **"Settings"** tab
2. Scroll to **"Domains"**
3. Click **"Generate Domain"**
4. Copy your Railway URL (e.g., `https://hackathon-ii-phase-three-production.up.railway.app`)

### Step 1.7: Test Backend

Open in browser:
```
https://your-railway-url.up.railway.app/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

**Test API Documentation:**
```
https://your-railway-url.up.railway.app/docs
```

You should see the FastAPI Swagger UI.

---

## 📦 Part 2: Vercel Frontend Deployment

### Step 2.1: Login to Vercel

1. Go to https://vercel.com/
2. Click **"Sign Up"** (if new) or **"Login"**
3. Click **"Continue with GitHub"**
4. Authorize Vercel to access your repositories

### Step 2.2: Import Project

1. From Vercel dashboard, click **"Add New..."** → **"Project"**
2. Find and select: `umairrafeeq303-create/hackathon-II-phase-three`
3. Click **"Import"**

### Step 2.3: Configure Build Settings

**IMPORTANT:** Set these correctly:

1. **Framework Preset**: Next.js (auto-detected)
2. **Root Directory**: Click **"Edit"** → Enter `frontend`
3. **Build Command**: `npm run build` (auto-filled)
4. **Output Directory**: `.next` (auto-filled)
5. **Install Command**: `npm install` (auto-filled)

### Step 2.4: Add Environment Variables

Before deploying, add environment variables:

1. Expand **"Environment Variables"** section
2. Add these variables:

**Variable 1:**
```
Name: NEXT_PUBLIC_API_URL
Value: https://your-railway-url.up.railway.app
```
Replace `your-railway-url.up.railway.app` with your actual Railway URL from Step 1.6

**Variable 2:**
```
Name: BETTER_AUTH_SECRET
Value: XghRTS6aptA9MGzVQ9pw1CFg05GPiX-45XE6FgaM8Jo
```
(This must match the backend BETTER_AUTH_SECRET exactly)

3. Click **"Deploy"**

### Step 2.5: Monitor Build

Watch the build logs:
- Installing dependencies
- Linting
- Type checking
- Building Next.js application
- Collecting page data
- Finalizing build

This takes 3-5 minutes.

### Step 2.6: Get Your Vercel URL

Once deployed:
1. You'll see **"Congratulations!"** screen
2. Copy your Vercel URL (e.g., `https://hackathon-ii-phase-three.vercel.app`)
3. Click **"Visit"** to open your app

---

## 🔗 Part 3: Update CORS Configuration

Now that frontend is deployed, update backend CORS:

### Step 3.1: Update Railway CORS_ORIGINS

1. Go back to **Railway Dashboard**
2. Click on your backend service
3. Go to **"Variables"** tab
4. Find `CORS_ORIGINS` variable
5. Click **"Edit"**
6. Update value to:

```
https://hackathon-ii-phase-three.vercel.app,https://hackathon-ii-phase-three-*.vercel.app
```

Replace `hackathon-ii-phase-three` with your actual Vercel project name.

7. Click **"Save"**
8. Railway will automatically redeploy (takes 1-2 minutes)

### Step 3.2: Why Two URLs?

- `https://hackathon-ii-phase-three.vercel.app` - Production URL
- `https://hackathon-ii-phase-three-*.vercel.app` - Preview deployments (when you push to branches)

---

## ✅ Part 4: Testing Your Deployment

### Test 1: Backend Health Check

```bash
curl https://your-railway-url.up.railway.app/health
```

**Expected:**
```json
{"status": "healthy"}
```

### Test 2: Backend API Docs

Open in browser:
```
https://your-railway-url.up.railway.app/docs
```

You should see FastAPI interactive documentation.

### Test 3: Frontend Homepage

1. Open your Vercel URL in browser
2. You should see the landing page

### Test 4: User Signup

1. Click **"Sign Up"** or **"Get Started"**
2. Enter:
   - Email: test@example.com
   - Password: TestPassword123
3. Click **"Sign Up"**
4. You should be redirected to dashboard

### Test 5: User Login

1. Log out
2. Click **"Login"**
3. Enter the credentials you just created
4. Click **"Login"**
5. You should be logged in

### Test 6: Task Management

1. Create a new task:
   - Title: "Test Task"
   - Description: "Testing deployment"
2. Click **"Add Task"**
3. Task should appear in your task list
4. Try editing the task
5. Try marking it as complete
6. Try deleting it

### Test 7: AI Chat Feature

1. Click on **"Chat"** or AI assistant icon
2. Type: "Show me all my tasks"
3. AI should respond with your task list
4. Try: "Create a task to buy groceries"
5. AI should create the task

---

## 🐛 Troubleshooting

### Problem: Railway shows "start.sh not found"

**Solution:**
The repository now has multiple start methods:
1. `start.sh` - Shell script
2. `Procfile` - Railway/Heroku standard
3. `nixpacks.toml` - Nixpacks configuration
4. `railway.json` - Railway-specific config

Railway will automatically choose the best method. If it still fails:

1. Go to Railway **Settings** → **Deploy**
2. Set **Start Command** manually:
   ```
   uvicorn src.main:app --host 0.0.0.0 --port $PORT
   ```

### Problem: "Error: Cannot find module 'next'"

**Solution:**
1. Check Vercel **Root Directory** is set to `frontend`
2. Verify **Install Command** is `npm install`
3. Redeploy

### Problem: Frontend shows "Failed to fetch" errors

**Solutions:**
1. Check `NEXT_PUBLIC_API_URL` environment variable in Vercel
2. Ensure it matches your Railway URL exactly (with https://)
3. No trailing slash in the URL
4. Redeploy Vercel after changing env vars

### Problem: CORS errors in browser console

**Solutions:**
1. Check Railway `CORS_ORIGINS` includes your Vercel URL
2. Must use `https://` not `http://`
3. Include both production and preview URLs
4. Wait for Railway to redeploy after changing CORS

### Problem: 500 Internal Server Error from backend

**Solutions:**
1. Check Railway logs: **Deployments** → Click latest → **View Logs**
2. Common issues:
   - DATABASE_URL incorrect
   - Missing environment variables
   - Database connection timeout
3. Verify all env vars are set correctly

### Problem: Authentication not working

**Solutions:**
1. Ensure `BETTER_AUTH_SECRET` is **exactly the same** on backend and frontend
2. Case-sensitive and character-sensitive
3. No extra spaces or quotes
4. Redeploy both if you changed it

---

## 📊 Deployment Checklist

### Railway Backend
- [ ] Root directory set to `backend`
- [ ] DATABASE_URL configured
- [ ] BETTER_AUTH_SECRET configured
- [ ] CORS_ORIGINS configured
- [ ] ENVIRONMENT set to `production`
- [ ] OPENAI_API_KEY configured
- [ ] PORT set to `8000`
- [ ] Deployment successful
- [ ] `/health` endpoint returns `{"status": "healthy"}`
- [ ] `/docs` shows API documentation

### Vercel Frontend
- [ ] Root directory set to `frontend`
- [ ] NEXT_PUBLIC_API_URL configured (Railway URL)
- [ ] BETTER_AUTH_SECRET configured (matches backend)
- [ ] Build successful
- [ ] Homepage loads correctly
- [ ] Can sign up new user
- [ ] Can login
- [ ] Can create/edit/delete tasks
- [ ] AI chat works

### Integration
- [ ] CORS_ORIGINS updated with Vercel URL
- [ ] No CORS errors in browser console
- [ ] Frontend can communicate with backend
- [ ] Authentication works end-to-end

---

## 🔄 Continuous Deployment

Both platforms are configured for automatic deployment:

### Railway
- **Trigger**: Push to `main` branch
- **Watches**: `backend/` directory
- **Build time**: ~2-3 minutes

### Vercel
- **Trigger**: Push to any branch
- **Main branch** → Production deployment
- **Other branches** → Preview deployments
- **Watches**: `frontend/` directory
- **Build time**: ~3-5 minutes

---

## 🎯 Production URLs

After successful deployment, save these URLs:

| Service | URL | Purpose |
|---------|-----|---------|
| **Backend API** | `https://your-app.up.railway.app` | API server |
| **API Docs** | `https://your-app.up.railway.app/docs` | API documentation |
| **Frontend** | `https://your-app.vercel.app` | Web application |
| **GitHub** | https://github.com/umairrafeeq303-create/hackathon-II-phase-three | Source code |

---

## 📞 Support Resources

- **Railway Docs**: https://docs.railway.app/
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs

---

## ✨ Next Steps

After successful deployment:

1. **Custom Domain** (Optional)
   - Add custom domain in Railway/Vercel settings
   - Update CORS_ORIGINS to include custom domain

2. **Monitoring**
   - Set up error tracking (Sentry)
   - Configure analytics
   - Set up uptime monitoring

3. **Database Backups**
   - Configure automatic Neon backups
   - Set up backup schedule

4. **Environment Variables Security**
   - Rotate BETTER_AUTH_SECRET periodically
   - Monitor API key usage
   - Set up API key rotation

---

**Deployment Complete!** 🎉

Your application is now live and ready for production use.
