# Setup Guide

This guide will help you set up the D&D Campaign Manager on your local machine or server.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR manually: Python 3.11+, Node.js 18+, PostgreSQL 14+

## Quick Start with Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd dnd_world
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file:**
   - Change `SECRET_KEY` to a secure random string
   - Adjust other settings as needed

4. **Start all services:**
   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Database: localhost:5432

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database:**
   - Create a PostgreSQL database named `dnd_world`
   - Update `DATABASE_URL` in `.env` file

5. **Create `.env` file in project root:**
   ```bash
   cp .env.example .env
   ```
   Then edit with your settings.

6. **Run database migrations:**
   ```bash
   alembic upgrade head
   ```
   Note: If this is the first run, tables will be auto-created by SQLAlchemy.

7. **Start the backend server:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

## First Steps

1. **Register a new account:**
   - Go to http://localhost:5173/register
   - Create your account

2. **Log in:**
   - Use your credentials to log in

3. **Create your first campaign:**
   - Click "Campaigns" in the navigation
   - Click "Create Campaign"

## D&D Beyond Integration

To import characters from D&D Beyond:

1. **Get your Cobalt token:**
   - Log in to D&D Beyond
   - Open browser DevTools (F12)
   - Go to Application/Storage → Cookies
   - Find `CobaltSession` cookie and copy its value

2. **Use the import endpoint:**
   - You can add this token when importing a character
   - Or set it as `DNDBEYOND_COBALT_TOKEN` in your `.env` file

Note: D&D Beyond does not have an official API, so this integration:
- Works with public character sheets (limited data)
- Requires your session token for private sheets
- May break if D&D Beyond changes their site structure

## Database Management

### Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Rollback migrations:
```bash
alembic downgrade -1
```

## Production Deployment

For production deployment:

1. **Update environment variables:**
   - Use a strong `SECRET_KEY`
   - Set `DATABASE_URL` to your production database
   - Update `ALLOWED_ORIGINS` with your frontend domain

2. **Use production ASGI server:**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. **Build frontend for production:**
   ```bash
   cd frontend
   npm run build
   ```
   Serve the `dist` folder with nginx or similar.

4. **Set up PostgreSQL backups**

5. **Use HTTPS with a reverse proxy (nginx)**

## Troubleshooting

### Database connection issues:
- Ensure PostgreSQL is running
- Check `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Verify database exists and user has permissions

### Port already in use:
- Change ports in `docker-compose.yml` or when running manually
- Backend default: 8000
- Frontend default: 5173
- Database default: 5432

### CORS errors:
- Ensure `ALLOWED_ORIGINS` in `.env` includes your frontend URL
- Check that both backend and frontend are running

### Module not found errors:
- Backend: Ensure virtual environment is activated and dependencies are installed
- Frontend: Run `npm install` again

## Support

For issues and questions:
- Check the main README.md
- Review API documentation at http://localhost:8000/docs
- Create an issue in the repository
