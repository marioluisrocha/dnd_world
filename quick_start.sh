#!/bin/bash

echo "========================================="
echo "D&D Campaign Manager - Quick Start"
echo "========================================="
echo ""

# Generate SECRET_KEY
echo "Generating SECRET_KEY..."
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Update .env file for SQLite
cat > .env << EOF
# Database (SQLite for development)
DATABASE_URL=sqlite:///./dnd_world.db

# Security
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Backend
API_V1_PREFIX=/api/v1
PROJECT_NAME=D&D Campaign Manager

# Frontend
VITE_API_URL=http://localhost:8000

# File Upload
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads

# D&D Beyond Integration (optional)
DNDBEYOND_COBALT_TOKEN=
EOF

echo "✓ Created .env with SQLite configuration"
echo ""

# Setup backend
echo "Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✓ Backend dependencies installed"
echo ""

# Initialize database
echo "Initializing database with sample data..."
python init_db.py --seed

echo "✓ Database initialized"
echo ""

cd ..

# Setup frontend
echo "Setting up frontend..."
cd frontend

if [ ! -f ".env" ]; then
    echo "VITE_API_URL=http://localhost:8000" > .env
fi

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies (this may take a few minutes)..."
    npm install
fi

echo "✓ Frontend dependencies installed"
echo ""

cd ..

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit:"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "Test login credentials:"
echo "  Username: dungeon_master"
echo "  Password: password123"
echo ""
