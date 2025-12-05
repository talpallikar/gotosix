import pytest
import mongomock
from app import create_app
from flask_pymongo import PyMongo

@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'

    yield app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture
def mongo(app, monkeypatch):
    """Create a mock MongoDB instance."""
    mock_client = mongomock.MongoClient()

    # Patch PyMongo to use mongomock
    def mock_init(self, app):
        self.db = mock_client['test_db']
        self.cx = mock_client

    monkeypatch.setattr(PyMongo, '__init__', mock_init)

    with app.app_context():
        mongo_instance = PyMongo(app)
        yield mongo_instance
        # Clear the database after each test
        mock_client.drop_database('test_db')

@pytest.fixture
def auth_headers(client, mongo):
    """Create a test user and return auth headers."""
    from auth import generate_token
    from bson import ObjectId
    from models import User

    user_id = ObjectId()
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        _id=user_id
    )

    mongo.db.users.insert_one({
        '_id': user._id,
        'username': user.username,
        'email': user.email,
        'password_hash': user.password_hash,
        'created_at': user.created_at
    })

    token = generate_token(user_id)

    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
