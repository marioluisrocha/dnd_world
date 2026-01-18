# 🚀 Ready to Deploy! Follow These Steps

Your code is on GitHub and ready to go! Here's exactly what to do:

## Step 1: Go to Render Dashboard

1. Open https://dashboard.render.com in your browser
2. Make sure you're logged in

## Step 2: Deploy Using Blueprint (Automatic - Easiest!)

1. Click the big **"New +"** button (top right)
2. Select **"Blueprint"**
3. Click **"Connect GitHub"** (if not already connected)
   - Authorize Render to access your repos
4. Find and select **"marioluisrocha/dnd_world"** repository
5. Render will automatically detect the `render.yaml` file!
6. Give it a name: **"D&D Campaign Manager"**
7. Click **"Apply"** button

## Step 3: Wait for Deployment (5-10 minutes)

Render will now create:
- ✅ PostgreSQL database
- ✅ Backend API service
- ✅ Frontend static site

Watch the progress:
- You'll see 3 services being created
- Each will show build logs
- Wait for all to show "Live" status (green dot)

## Step 4: Configure Environment Variables

### A. Update Backend CORS

1. In dashboard, click on **"dnd-backend"** service
2. Go to **"Environment"** tab on the left
3. Find `ALLOWED_ORIGINS` variable
4. Click **"Edit"**
5. Look at your frontend service URL (something like `https://dnd-frontend-xyz.onrender.com`)
6. Set `ALLOWED_ORIGINS` to that exact URL (no trailing slash!)
7. Click **"Save Changes"**
8. Service will redeploy automatically (~2 minutes)

### B. Update Frontend API URL

1. In dashboard, click on **"dnd-frontend"** service
2. Go to **"Environment"** tab
3. Find `VITE_API_URL` variable
4. Click **"Edit"**
5. Look at your backend service URL (something like `https://dnd-backend-xyz.onrender.com`)
6. Set `VITE_API_URL` to that exact URL (no trailing slash!)
7. Click **"Save Changes"**
8. Service will redeploy automatically (~2 minutes)

## Step 5: Get Your URLs!

Once both redeployments finish:

1. Click on **"dnd-frontend"** service
2. At the top, you'll see your URL: `https://dnd-frontend-xyz.onrender.com`
3. **Copy this URL** - this is what you'll share!

## Step 6: Test Your App!

1. Visit your frontend URL
2. Click **"Register"**
3. Create an account
4. Login
5. Try creating a campaign!

## Step 7: Share with Friends! 🎉

Send them your frontend URL:
`https://dnd-frontend-xyz.onrender.com`

They can:
- Register their own accounts
- Join your campaigns
- Start playing D&D online!

---

## Troubleshooting

### If Blueprint deployment fails:

Use Manual Deployment (see [RENDER_DEPLOY_STEPS.md](RENDER_DEPLOY_STEPS.md) - "Option B")

### If you see errors:

1. Check logs: Service → **Logs** tab
2. Most common issues:
   - Environment variables not set correctly
   - CORS mismatch (backend ALLOWED_ORIGINS vs frontend URL)
   - Database not ready yet

### CORS Error in Browser:

**Symptom:** Console shows "CORS policy" error

**Fix:**
1. Backend → Environment → `ALLOWED_ORIGINS`
2. Must EXACTLY match frontend URL (with https://, no trailing slash)
3. Example: `https://dnd-frontend-abc123.onrender.com`

### App loads but can't register:

**Check:**
1. Backend logs (look for errors)
2. Database is running (green dot)
3. `VITE_API_URL` points to correct backend URL

### Database initialization didn't run:

If tables aren't created:
1. Go to backend service → **Shell** tab
2. Run: `python init_db.py`
3. This creates all database tables

---

## Important Notes

⚠️ **First Visit After Idle = 15 Seconds**
- Free tier services sleep after 15 minutes
- First visit wakes them up
- This is NORMAL - not a bug!

⚠️ **Database Expires in 90 Days**
- Free PostgreSQL databases expire
- Back up your data!
- Command: `pg_dump <DB_URL> > backup.sql`

✅ **Auto-Deploy on Git Push**
- Any time you `git push`, Render auto-deploys
- No manual updates needed!

---

## Quick Reference

**Your Services:**
- Database: `dnd-db`
- Backend: `dnd-backend`
- Frontend: `dnd-frontend`

**Dashboard:** https://dashboard.render.com

**Your GitHub Repo:** https://github.com/marioluisrocha/dnd_world

**Need Help?** Check [RENDER_DEPLOY_STEPS.md](RENDER_DEPLOY_STEPS.md) for detailed troubleshooting

---

## Success Checklist ✅

- [ ] Blueprint deployed (3 services created)
- [ ] Backend ALLOWED_ORIGINS set to frontend URL
- [ ] Frontend VITE_API_URL set to backend URL
- [ ] All services show "Live" (green dot)
- [ ] Can visit frontend URL
- [ ] Can register a user
- [ ] Can login
- [ ] Can create a campaign

**All checked? You're LIVE! 🎉**

Share your URL and start playing D&D with your friends!
