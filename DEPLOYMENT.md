# Free Deployment Options for D&D Campaign Manager

## Recommended: Railway.app (Best for Full-Stack Apps)

**Pros:**
- Free tier: $5 credit/month (enough for small projects)
- Supports PostgreSQL database
- Easy deployment from GitHub
- Auto HTTPS
- Custom domains

**Cons:**
- Requires credit card for verification
- Limited to $5/month free tier

### Steps:

1. **Push to GitHub** (if not already)
2. **Sign up at** https://railway.app
3. **New Project → Deploy from GitHub**
4. **Add PostgreSQL** from Railway's service catalog
5. **Set environment variables** in Railway dashboard
6. **Deploy!**

---

## Option 2: Render.com (Generous Free Tier)

**Pros:**
- Truly free tier (no credit card required)
- PostgreSQL database included
- Auto HTTPS
- Good for production

**Cons:**
- Free tier services spin down after 15 minutes of inactivity (cold starts)
- Slower than paid options

### Steps:

1. **Create account** at https://render.com
2. **New → Web Service** (for backend)
3. **New → Static Site** (for frontend)
4. **New → PostgreSQL** (free database)
5. **Configure and deploy**

---

## Option 3: Fly.io (Developer Friendly)

**Pros:**
- Generous free tier
- Multiple regions
- Good documentation
- Fast deployments

**Cons:**
- Requires credit card
- CLI-based deployment

### Steps:

1. **Install Fly CLI**: `curl -L https://fly.io/install.sh | sh`
2. **Sign up**: `flyctl auth signup`
3. **Deploy backend**: `flyctl launch`
4. **Add PostgreSQL**: `flyctl postgres create`
5. **Deploy frontend** separately or as static assets

---

## Option 4: Vercel (Frontend) + Supabase (Backend/DB)

**Pros:**
- No credit card required
- Excellent performance
- Supabase gives you PostgreSQL + auth
- Perfect for this stack

**Cons:**
- Need to migrate from FastAPI to Vercel serverless functions OR keep backend elsewhere
- More complex setup

---

## My Recommendation: **Render.com** (Easiest & Free)

Let me guide you through deploying to Render.com:

## Complete Render.com Deployment Guide

### Prerequisites

1. **GitHub Account** - Create one at https://github.com if you don't have it
2. **Render Account** - Sign up at https://render.com (free, no credit card)

### Step 1: Push Your Code to GitHub

```bash
# Initialize git (if not already)
cd /home/mario/code/marioluisrocha/dnd_world
git init

# Create .gitignore (already exists)
# Add all files
git add .

# Commit
git commit -m "Initial commit - D&D Campaign Manager"

# Create a new repository on GitHub (via web interface)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/dnd-campaign-manager.git
git branch -M main
git push -u origin main
```

### Step 2: Prepare for Deployment

Create a `render.yaml` file for automatic deployment:

```yaml
# render.yaml - Blueprint for Render deployment
databases:
  - name: dnd-db
    plan: free
    databaseName: dnd_world
    user: dnd_user

services:
  # Backend API
  - type: web
    name: dnd-backend
    runtime: python
    plan: free
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: dnd-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ALGORITHM
        value: HS256
      - key: ACCESS_TOKEN_EXPIRE_MINUTES
        value: 10080
      - key: ALLOWED_ORIGINS
        sync: false # Set this manually after frontend is deployed
      - key: PYTHON_VERSION
        value: 3.11.0

  # Frontend
  - type: web
    name: dnd-frontend
    runtime: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/dist
    envVars:
      - key: VITE_API_URL
        sync: false # Set this manually after backend is deployed
```

### Step 3: Deploy to Render

#### Option A: Using Blueprint (render.yaml)

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

#### Option B: Manual Setup (More Control)

**Deploy PostgreSQL Database:**
1. Dashboard → **"New +"** → **"PostgreSQL"**
2. Name: `dnd-db`
3. Database: `dnd_world`
4. Plan: **Free**
5. Click **"Create Database"**
6. **Copy the Internal Database URL** (you'll need this)

**Deploy Backend:**
1. Dashboard → **"New +"** → **"Web Service"**
2. Connect your GitHub repo
3. Name: `dnd-backend`
4. Runtime: **Python 3**
5. Build Command: `cd backend && pip install -r requirements.txt`
6. Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Plan: **Free**
8. **Environment Variables:**
   - `DATABASE_URL` = (paste Internal Database URL from step 1)
   - `SECRET_KEY` = (generate random string)
   - `ALGORITHM` = `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `10080`
   - `ALLOWED_ORIGINS` = `https://your-frontend-url.onrender.com`
   - `PYTHON_VERSION` = `3.11.0`
9. Click **"Create Web Service"**
10. **Copy your backend URL** (e.g., `https://dnd-backend.onrender.com`)

**Deploy Frontend:**
1. Dashboard → **"New +"** → **"Static Site"**
2. Connect your GitHub repo
3. Name: `dnd-frontend`
4. Build Command: `cd frontend && npm install && npm run build`
5. Publish Directory: `frontend/dist`
6. **Environment Variables:**
   - `VITE_API_URL` = `https://dnd-backend.onrender.com` (your backend URL)
7. Click **"Create Static Site"**

### Step 4: Update CORS Settings

After both are deployed:

1. Go to your **backend service** on Render
2. **Environment** tab → Edit `ALLOWED_ORIGINS`
3. Add your frontend URL: `https://your-frontend-name.onrender.com`
4. Save (this will trigger a redeploy)

### Step 5: Initialize Database

Once backend is deployed:

```bash
# Connect to your Render shell
# Go to backend service → Shell tab
python init_db.py
```

Or use the external database URL to connect locally:
```bash
psql "YOUR_EXTERNAL_DATABASE_URL"
```

### Step 6: Test Your Deployment!

Visit your frontend URL: `https://your-frontend-name.onrender.com`

---

## Security Considerations for Public Deployment

### Must-Do Before Going Live:

1. **Change SECRET_KEY**
   - Generate a new, random secret key for production
   - Never use the same key as development

2. **Enable HTTPS Only**
   - Render provides this automatically
   - Ensure `ALLOWED_ORIGINS` only includes HTTPS URLs

3. **Set Up Rate Limiting**
   - Add to `backend/app/main.py`:
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   ```

4. **Add Input Validation**
   - Already done with Pydantic schemas ✓

5. **Set Up Monitoring**
   - Use Render's built-in logging
   - Monitor for unusual activity

6. **Backup Database**
   - Render free tier doesn't include automatic backups
   - Manually export data regularly:
   ```bash
   pg_dump DATABASE_URL > backup.sql
   ```

### Optional Enhancements:

- **Custom Domain**: Add your own domain in Render dashboard
- **Environment-based Config**: Different settings for dev/prod
- **Database Migrations**: Use Alembic for schema changes
- **Email Notifications**: Add email service for user registration

---

## Cost Breakdown (Free Tiers)

### Render.com Free Plan:
- ✅ 750 hours/month (enough for 1 service)
- ✅ PostgreSQL database (90 days, then expires - backup needed!)
- ✅ Auto sleep after 15 min inactivity
- ✅ HTTPS included
- ⚠️ Slower cold starts

### Railway.app Free Plan:
- ✅ $5 credit/month
- ✅ PostgreSQL included
- ✅ No sleep time
- ✅ Faster performance
- ⚠️ Requires credit card

### Fly.io Free Plan:
- ✅ 3 shared VMs
- ✅ 3GB persistent storage
- ✅ Good performance
- ⚠️ Requires credit card

---

## Troubleshooting Common Issues

### Backend won't start
- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure `PYTHON_VERSION` is set

### Frontend can't connect to backend
- Check `ALLOWED_ORIGINS` in backend env vars
- Verify `VITE_API_URL` in frontend env vars
- Check browser console for CORS errors

### Database connection fails
- Verify `DATABASE_URL` is correct
- Check if using Internal vs External URL
- Ensure database is running

### Cold starts (15-second delay)
- This is normal on free tier
- Backend wakes up after first request
- Consider upgrading to paid tier if needed

---

## Sharing with Friends

Once deployed, share:
1. **Frontend URL**: `https://your-app.onrender.com`
2. **Tell them to register** an account
3. **Create a campaign** and add them as members
4. **Enjoy!** 🎲

---

## Monitoring & Maintenance

### Check Service Health:
- Render Dashboard → Your Services → Logs
- Monitor for errors
- Check resource usage

### Database Backups (Important!):
Free PostgreSQL on Render expires after 90 days. Back up regularly:

```bash
# Using Render dashboard Shell or locally:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

### Updates:
Just push to GitHub:
```bash
git add .
git commit -m "Update features"
git push
```
Render auto-deploys on push!

---

## Need Help?

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Your app logs: Check Render dashboard → Logs tab
