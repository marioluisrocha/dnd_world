# Quick Share with Ngrok (Free, No Signup for Basic)

## What is Ngrok?
Ngrok creates a public URL that tunnels to your local machine. Perfect for quick testing with friends!

## Setup (5 minutes)

### Step 1: Install Ngrok

```bash
# Download and install
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update
sudo apt install ngrok
```

### Step 2: Get Free Account (Optional but Recommended)

1. Go to https://dashboard.ngrok.com/signup
2. Sign up (free, with Google/GitHub)
3. Copy your authtoken
4. Run: `ngrok config add-authtoken YOUR_TOKEN`

### Step 3: Start Your Services

```bash
# Terminal 1: Backend
cd /home/mario/code/marioluisrocha/dnd_world/backend
source ../venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd /home/mario/code/marioluisrocha/dnd_world/frontend
npm run dev -- --host 0.0.0.0 --port 5173
```

### Step 4: Create Tunnels

```bash
# Terminal 3: Backend tunnel
ngrok http 8000

# Terminal 4: Frontend tunnel
ngrok http 5173
```

### Step 5: Update CORS

Ngrok will give you URLs like:
- Backend: `https://abc123.ngrok.io`
- Frontend: `https://xyz789.ngrok.io`

Update backend `.env`:
```bash
ALLOWED_ORIGINS=https://xyz789.ngrok.io
```

Restart backend server.

### Step 6: Share!

Send your friends the **frontend URL**: `https://xyz789.ngrok.io`

## Pros & Cons

✅ **Pros:**
- Free (with limits)
- No deployment needed
- Instant sharing
- Your computer stays in control

❌ **Cons:**
- Requires your computer to stay on
- URL changes each time (free tier)
- Limited to 40 connections/minute (free tier)
- Not suitable for long-term hosting

## Perfect For:
- Quick testing with friends
- Game night sessions
- Demo purposes
- Before committing to a hosting platform

## Upgrade to Permanent Later

When ready for 24/7 hosting, switch to Railway or Render using the guides provided!
