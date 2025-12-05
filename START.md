# Getting Started - MTG Mulligan Trainer

Quick guide to get the application running locally.

## Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+**, **Node.js 20+**, and **MongoDB** (for manual setup)

## Option 1: Docker (Recommended) ⚡

The easiest way to run everything:

```bash
# Navigate to project directory
cd gotosix

# Start all services
docker-compose up --build
```

**That's it!** Wait for services to start, then:
- **Open app:** http://localhost
- **Backend API:** http://localhost:5000

**To stop:**
```bash
# Press Ctrl+C, then:
docker-compose down
```

## Option 2: Manual Setup (Development) 💻

### Prerequisites
1. Install MongoDB locally or run:
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo:7
   ```

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env if needed (default MongoDB URI: mongodb://localhost:27017/mtg_mulligan)

# Run backend
python app.py
```

✅ Backend running at: http://localhost:5000

### Frontend Setup

**Open a new terminal:**

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

✅ Frontend running at: http://localhost:5173

## Using the Application

### 1. Register an Account
- Go to http://localhost (or :5173)
- Click "Register" in the navigation
- Create your account

### 2. Upload a Decklist
- Click "Upload Decklist"
- Fill in deck details:
  - **Name:** Mono Red Aggro
  - **Format:** Modern
  - **Decklist:** (one card per line)
    ```
    4 Lightning Bolt
    4 Monastery Swiftspear
    4 Goblin Guide
    4 Eidolon of the Great Revel
    20 Mountain
    4 Lava Spike
    ```

### 3. Create Mulligan Scenarios
- Click "Create Scenario"
- Select your decklist
- Choose:
  - Number of cards (7 for opening hand)
  - Play/Draw
  - Opponent archetype
  - Game number
- Click "Create Scenario"

### 4. Vote on Scenarios
- Browse scenarios on the "Scenarios" page
- View mulligan scenarios with actual card images
- Vote "Keep" or "Mulligan" to help the community learn!

## Quick Commands Reference

### Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Clean restart
docker-compose down -v
docker-compose up --build
```

### Development Commands

```bash
# Backend (from backend/)
python app.py                    # Run server
pytest                          # Run tests
pytest --cov                    # Run tests with coverage

# Frontend (from frontend/)
npm run dev                     # Run dev server
npm run build                   # Build for production
npm test                        # Run tests
npm run test:coverage           # Run tests with coverage
```

## Troubleshooting

### "Port already in use" Error

```bash
# Find what's using the port
lsof -i :5000   # Backend
lsof -i :80     # Frontend (Docker)
lsof -i :5173   # Frontend (Dev)

# Kill the process or change port in docker-compose.yml
```

### MongoDB Connection Failed

```bash
# Check if MongoDB is running
docker ps | grep mongo

# Start MongoDB if not running
docker run -d -p 27017:27017 --name mongodb mongo:7

# Or restart MongoDB container
docker restart mongodb
```

### Frontend Can't Reach Backend

**If using Docker:**
- Make sure all containers are running: `docker-compose ps`
- Restart: `docker-compose restart`

**If running manually:**
- Ensure backend is running on port 5000
- Check frontend proxy settings in `vite.config.js`

### Docker Build Issues

```bash
# Clean everything and rebuild
docker-compose down -v
docker system prune -f
docker-compose up --build
```

### Backend Import Errors

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # You should see (venv) in prompt

# Reinstall dependencies
pip install -r requirements.txt
```

## Development Tips

✨ **Hot Reload:**
- Backend auto-reloads when you save Python files (debug mode)
- Frontend hot-reloads instantly with Vite

🗄️ **View Database:**
- Install [MongoDB Compass](https://www.mongodb.com/products/compass)
- Connect to: `mongodb://localhost:27017`
- Browse collections: users, decklists, scenarios, votes

🧪 **Running Tests:**
```bash
# Backend tests
cd backend
pip install -r requirements-test.txt
pytest -v

# Frontend tests
cd frontend
npm test
```

🐛 **Debugging:**
- Backend logs show in terminal or `docker-compose logs backend`
- Frontend dev tools: F12 in browser
- Check Network tab for API calls

## Next Steps

- 📖 Read the full [README.md](README.md) for detailed documentation
- 🧪 Check [TESTING.md](TESTING.md) for testing guide
- 🎯 Start creating mulligan scenarios and voting!

## Need Help?

Common issues:
1. **Cards not loading images?** - Scryfall API might be rate-limiting, wait a moment
2. **Can't login?** - Check browser console for errors
3. **Votes not updating?** - Make sure you're logged in

For more help, check the logs:
```bash
# Docker
docker-compose logs backend
docker-compose logs frontend

# Manual
# Check terminal where you ran python app.py or npm run dev
```

---

**Ready to test your mulligan skills!** 🎴✨
