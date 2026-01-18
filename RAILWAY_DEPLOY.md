# Railway.app Deployment Guide (100% Free, No Credit Card Required)

## Why Railway?
- ✅ $5 free credit per month (enough for this project)
- ✅ NO credit card required to start
- ✅ PostgreSQL database included
- ✅ Auto-deploy from GitHub
- ✅ Simple setup

## Step 1: Push to GitHub (if not done)

```bash
cd /home/mario/code/marioluisrocha/dnd_world
git add .
git commit -m "Add Railway deployment config"
git push origin main
```

## Step 2: Deploy to Railway

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select **marioluisrocha/dnd_world** repository

## Step 3: Add Database

1. In your project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will create a PostgreSQL database
4. Copy the **DATABASE_URL** from the database settings

## Step 4: Configure Backend Service

1. Click on your **backend service** (auto-detected from repo)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add these:

```
DATABASE_URL = ${{Postgres.DATABASE_URL}}
SECRET_KEY = (generate with: openssl rand -hex 32)
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
API_V1_PREFIX = /api/v1
PROJECT_NAME = D&D Campaign Manager
ALLOWED_ORIGINS = (leave blank for now, will update after frontend deploys)
```

4. Go to **"Settings"** tab
5. **Root Directory**: `backend`
6. **Build Command**: `pip install -r requirements.txt`
7. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. Click **"Deploy"**

## Step 5: Configure Frontend Service

1. Click **"+ New"** → **"GitHub Repo"** → Select same repo
2. This creates a second service from the same repo
3. Go to **"Variables"** tab
4. Add variable:
```
VITE_API_URL = (your backend URL from step 4)
```

5. Go to **"Settings"** tab
6. **Root Directory**: `frontend`
7. **Build Command**: `npm install && npm run build`
8. **Start Command**: `npx serve -s dist -p $PORT`
9. Click **"Deploy"**

## Step 6: Update CORS

1. Go back to **backend service**
2. **Variables** tab
3. Edit **ALLOWED_ORIGINS**
4. Set to your frontend URL (from step 5)
5. Service will auto-redeploy

## Step 7: Initialize Database

1. Click on **backend service**
2. Go to **"Settings"** → **"Service"**
3. Scroll to **"Custom Start Command"**
4. Temporarily change to: `python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. After deployment succeeds, change it back to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Your URLs

- **Frontend**: `https://your-frontend.railway.app`
- **Backend**: `https://your-backend.railway.app`

Share the frontend URL with your friends!

## Important Notes

📊 **Free Tier Limits:**
- $5 credit per month
- ~500 hours of usage
- Perfect for small projects like this

⏰ **No Sleep:**
- Unlike Render, Railway doesn't sleep services
- Your app stays fast 24/7

🔄 **Auto-Deploy:**
- Every `git push` auto-deploys
- No manual updates needed

## Troubleshooting

### If build fails:
- Check logs in Railway dashboard
- Verify Root Directory is set correctly
- Ensure environment variables are set

### If CORS errors:
- Backend ALLOWED_ORIGINS must exactly match frontend URL
- Include `https://`, no trailing slash

### If database connection fails:
- Verify DATABASE_URL is using Railway's Postgres variable
- Check database service is running (green indicator)

---

## Success Checklist

- [ ] Railway account created (no credit card needed)
- [ ] PostgreSQL database added
- [ ] Backend service deployed
- [ ] Frontend service deployed
- [ ] Environment variables configured
- [ ] CORS configured
- [ ] Database initialized
- [ ] Can access frontend URL
- [ ] Can register and login

**All checked? You're LIVE! 🎉**
