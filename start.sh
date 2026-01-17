#!/bin/bash

# D&D Campaign Manager - Quick Start Script

echo "====================================="
echo "D&D Campaign Manager - Setup"
echo "====================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env

    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32)

    # Update the .env file with the generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    fi

    echo "✓ Created .env file with generated SECRET_KEY"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "Choose setup method:"
echo "1) Docker (recommended)"
echo "2) Manual setup"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "Starting with Docker..."
    echo ""

    # Check if docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker and try again."
        exit 1
    fi

    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi

    echo "Building and starting containers..."
    docker-compose up --build -d

    echo ""
    echo "====================================="
    echo "Setup Complete!"
    echo "====================================="
    echo ""
    echo "Services are starting up..."
    echo "- Frontend: http://localhost:5173"
    echo "- Backend API: http://localhost:8000"
    echo "- API Docs: http://localhost:8000/docs"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    echo ""

elif [ "$choice" = "2" ]; then
    echo ""
    echo "Manual setup selected..."
    echo ""

    # Backend setup
    echo "Setting up backend..."
    cd backend

    if [ ! -d "venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi

    echo "Activating virtual environment..."
    source venv/bin/activate

    echo "Installing Python dependencies..."
    pip install -r requirements.txt

    echo "✓ Backend setup complete"
    echo ""

    # Frontend setup
    cd ../frontend
    echo "Setting up frontend..."

    if [ ! -f ".env" ]; then
        cp .env.example .env
    fi

    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    fi

    echo "✓ Frontend setup complete"
    echo ""

    cd ..

    echo "====================================="
    echo "Manual Setup Complete!"
    echo "====================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Ensure PostgreSQL is running"
    echo "2. Create database: createdb dnd_world"
    echo "3. Update DATABASE_URL in .env if needed"
    echo ""
    echo "To start the backend:"
    echo "  cd backend"
    echo "  source venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    echo ""
    echo "To start the frontend (in another terminal):"
    echo "  cd frontend"
    echo "  npm run dev"
    echo ""
else
    echo "Invalid choice. Exiting."
    exit 1
fi
