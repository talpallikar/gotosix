# MTG Mulligan Trainer

A full-stack web application for practicing mulligan decisions in Magic: The Gathering. Users can upload decklists, generate mulligan scenarios, and vote on Keep or Mulligan decisions to help the community learn optimal mulligan strategies.

**📚 Quick Links:**
- [Getting Started](START.md) - How to run the app locally
- [Testing Guide](TESTING.md) - Running tests and coverage

## Features

- **User Authentication**: JWT-based authentication system for secure user management
- **Decklist Management**: Upload and browse decklists in various formats
- **Scenario Generation**: Automatically generate realistic mulligan scenarios from any decklist
- **Community Voting**: Vote on Keep or Mulligan decisions and see what the community thinks
- **Comprehensive Metadata**: Track important details like play/draw, opponent archetype, and game number

## Tech Stack

### Backend
- Flask (Python web framework)
- MongoDB (NoSQL database)
- JWT (Authentication)
- Flask-CORS (Cross-origin resource sharing)

### Frontend
- Vue.js 3 (Progressive JavaScript framework)
- Vue Router (Routing)
- Pinia (State management)
- Vite (Build tool)

### Infrastructure
- Docker & Docker Compose
- Nginx (Reverse proxy and static file serving)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git (to clone the repository)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gotosix
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env and set a secure SECRET_KEY for production
```

3. Start the application:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost
- Backend API: http://localhost:5000
- MongoDB: localhost:27017

### First Time Setup

1. Register a new account at http://localhost/register
2. Upload a decklist at http://localhost/decklists/new
3. Create mulligan scenarios at http://localhost/scenarios/new
4. Vote on scenarios and help the community learn!

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The backend will run on http://localhost:5000

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on http://localhost:3000

## Testing

The project includes comprehensive tests for both backend and frontend. See [TESTING.md](TESTING.md) for detailed information.

### Quick Start

**Backend Tests:**
```bash
cd backend
pip install -r requirements-test.txt
pytest
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

**Test Coverage:**
```bash
# Backend
pytest --cov

# Frontend
npm run test:coverage
```

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://mongodb:27017/mtg_mulligan
JWT_EXPIRATION_HOURS=24
FLASK_ENV=development
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token

### Decklists
- `GET /api/decklists` - Get all public decklists
- `GET /api/decklists/:id` - Get a specific decklist
- `GET /api/decklists/my` - Get current user's decklists (requires auth)
- `POST /api/decklists` - Create a new decklist (requires auth)

### Scenarios
- `GET /api/scenarios` - Get all scenarios (paginated)
- `GET /api/scenarios/:id` - Get a specific scenario
- `POST /api/scenarios` - Create a new scenario (requires auth)

### Votes
- `POST /api/votes` - Vote on a scenario (requires auth)
- `GET /api/votes/scenario/:id` - Get current user's vote for a scenario (requires auth)

## Project Structure

```
gotosix/
├── backend/
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── decklist_routes.py
│   │   ├── scenario_routes.py
│   │   └── vote_routes.py
│   ├── app.py
│   ├── models.py
│   ├── auth.py
│   ├── config.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── views/
│   │   ├── router/
│   │   ├── store/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vite.config.js
│   ├── nginx.conf
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Production Deployment

For production deployment:

1. Change `SECRET_KEY` in `.env` to a secure random string
2. Set `FLASK_ENV=production` in docker-compose.yml
3. Configure proper MongoDB authentication
4. Use a reverse proxy (nginx/Caddy) with SSL/TLS
5. Set up proper backup strategies for MongoDB

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.
