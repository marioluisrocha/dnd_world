# Render.com Deployment - Step by Step Guide

## What You Have Ready:
✅ GitHub repository created
✅ Render.com account ready
✅ `render.yaml` configuration file
✅ Build scripts prepared

## Deployment Steps

### Step 1: Push Your Code to GitHub

```bash
cd /home/mario/code/marioluisrocha/dnd_world

# Check git status
git status

# Add all files
git add .

# Commit changes
git commit -m "Add Render deployment configuration"

# Push to GitHub (replace with your repo URL)
git push origin main
```

If you haven't connected to GitHub yet:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Using Render Blueprint

**Option A: Automatic (Recommended)**

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. **Connect your GitHub repository**
   - Click "Connect GitHub" if not already connected
   - Select your `dnd_world` repository
4. Render will detect `render.yaml` automatically
5. Give your blueprint a name: **"D&D Campaign Manager"**
6. Click **"Apply"**
7. Wait for deployment (5-10 minutes)

**Render will automatically create:**
- PostgreSQL database (`dnd-db`)
- Backend service (`dnd-backend`)
- Frontend service (`dnd-frontend`)

### Step 3: Configure Environment Variables

After blueprint deploys, you need to set CORS:

**Backend Service:**
1. Go to **Dashboard** → **dnd-backend** → **Environment**
2. Find `ALLOWED_ORIGINS`
3. Click **"Edit"**
4. Set value to: `https://dnd-frontend.onrender.com` (or your actual frontend URL)
5. Click **"Save Changes"** (will trigger redeploy)

**Frontend Service:**
1. Go to **Dashboard** → **dnd-frontend** → **Environment**
2. Find `VITE_API_URL`
3. Click **"Edit"**
4. Set value to: `https://dnd-backend.onrender.com` (or your actual backend URL)
5. Click **"Save Changes"** (will trigger redeploy)

### Step 4: Wait for Deployment

Monitor the deployment:
- Go to each service → **Logs** tab
- Watch for "Deploy succeeded" message
- Backend should show: "Application startup complete"
- Frontend should show: "Build completed"

### Step 5: Test Your Application!

1. Get your frontend URL from Render dashboard
   - Should be something like: `https://dnd-frontend.onrender.com`
2. Visit the URL in your browser
3. Register a new account
4. Login and test!

---

## Option B: Manual Deployment (If Blueprint Doesn't Work)

### 1. Deploy PostgreSQL Database

1. Render Dashboard → **"New +"** → **"PostgreSQL"**
2. **Name**: `dnd-db`
3. **Database**: `dnd_world`
4. **User**: `dnd_user`
5. **Region**: Choose closest to you
6. **Plan**: **Free**
7. Click **"Create Database"**
8. **Copy the "Internal Database URL"** - you'll need this!

### 2. Deploy Backend

1. Render Dashboard → **"New +"** → **"Web Service"**
2. **Connect GitHub repository**
3. **Name**: `dnd-backend`
4. **Root Directory**: `backend`
5. **Runtime**: **Python 3**
6. **Build Command**: `pip install -r requirements.txt`
7. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
8. **Plan**: **Free**

**Environment Variables** (click "Add Environment Variable"):
```
DATABASE_URL = <paste Internal Database URL from database>
SECRET_KEY = <generate random string - use: openssl rand -hex 32>
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 10080
ALLOWED_ORIGINS = <leave blank for now, fill after frontend deploys>
API_V1_PREFIX = /api/v1
PROJECT_NAME = D&D Campaign Manager
PYTHON_VERSION = 3.11.0
```

9. Click **"Create Web Service"**
10. **Copy your backend URL** (e.g., `https://dnd-backend-xyz.onrender.com`)

### 3. Deploy Frontend

1. Render Dashboard → **"New +"** → **"Static Site"**
2. **Connect GitHub repository**
3. **Name**: `dnd-frontend`
4. **Root Directory**: `frontend`
5. **Build Command**: `npm install && npm run build`
6. **Publish Directory**: `dist`

**Environment Variables**:
```
VITE_API_URL = <paste your backend URL from step 2>
```

7. Click **"Create Static Site"**

### 4. Update CORS on Backend

1. Go back to **dnd-backend** service
2. **Environment** tab
3. Edit `ALLOWED_ORIGINS`
4. Set to your frontend URL: `https://dnd-frontend-xyz.onrender.com`
5. **Save** (will redeploy)

---

## Troubleshooting

### Backend won't start

**Check logs:**
- Render Dashboard → dnd-backend → Logs

**Common issues:**
- Missing environment variables
- Database connection failed
- Python version mismatch

**Fix:**
```bash
# Ensure PYTHON_VERSION is set to 3.11.0
# Verify DATABASE_URL is correct
# Check all required env vars are set
```

### Frontend shows blank page

**Check browser console:**
- Right-click → Inspect → Console

**Common issues:**
- API URL not set correctly
- CORS error (backend ALLOWED_ORIGINS not set)

**Fix:**
- Verify `VITE_API_URL` is your backend URL
- Verify backend `ALLOWED_ORIGINS` includes frontend URL

### Database connection fails

**Check:**
- DATABASE_URL is the **Internal** URL (starts with `postgresql://`)
- Database service is running (green dot in dashboard)

### CORS errors

**Symptoms:**
- Browser console shows: "CORS policy: No 'Access-Control-Allow-Origin'"

**Fix:**
1. Backend → Environment → `ALLOWED_ORIGINS`
2. Must match your frontend URL exactly (including https://)
3. No trailing slash

### Cold start (15-second delay on first visit)

**This is normal for free tier!**
- Services sleep after 15 minutes of inactivity
- First request wakes them up (~15 seconds)
- Subsequent requests are fast

**Not a bug - just how free tier works.**

---

## After Deployment

### Get Your URLs

**Frontend:** https://dnd-frontend-[random].onrender.com
**Backend:** https://dnd-backend-[random].onrender.com

### Share with Friends

Send them the **frontend URL** only. They can:
1. Register an account
2. Create campaigns
3. Start playing D&D!

### Monitor Your App

**Check logs:**
- Dashboard → Services → Logs tab

**Database management:**
- Dashboard → dnd-db → Info tab
- Can connect with psql using External Database URL

### Important Notes

⚠️ **Free Database Expires in 90 Days**
- Back up your data regularly
- Export with: `pg_dump <EXTERNAL_DB_URL> > backup.sql`

⚠️ **Services Sleep After 15 Minutes**
- Normal behavior for free tier
- First visit after idle = ~15 seconds to wake up

✅ **Auto-Deploy on Git Push**
- Just `git push` and Render auto-deploys
- No manual updates needed

---

## Custom Domain (Optional)

Want your own domain?

1. Buy domain (Namecheap, GoDaddy, etc.)
2. Render Dashboard → dnd-frontend → Settings
3. **Custom Domains** → **Add Custom Domain**
4. Follow DNS setup instructions
5. Update backend `ALLOWED_ORIGINS` to include new domain

---

## Need Help?

- **Render Status**: https://status.render.com
- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Your Logs**: Dashboard → Service → Logs tab

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Database deployed (green status)
- [ ] Backend deployed (green status)
- [ ] Frontend deployed (green status)
- [ ] ALLOWED_ORIGINS set on backend
- [ ] VITE_API_URL set on frontend
- [ ] Can register a user
- [ ] Can login
- [ ] Can create a campaign

If all checked ✅ - **You're live!** 🎉
