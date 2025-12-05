import pytest
import json

class TestAuthAPI:
    def test_register_success(self, client, mongo):
        """Test successful user registration."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['message'] == 'User registered successfully'
        assert 'token' in json_data
        assert json_data['user']['username'] == 'newuser'
        assert json_data['user']['email'] == 'newuser@example.com'

    def test_register_duplicate_email(self, client, mongo):
        """Test registration with duplicate email."""
        data = {
            'username': 'user1',
            'email': 'test@example.com',
            'password': 'password123'
        }

        # First registration
        client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        # Attempt duplicate registration
        data['username'] = 'user2'
        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        json_data = response.get_json()
        assert 'already registered' in json_data['message'].lower()

    def test_register_duplicate_username(self, client, mongo):
        """Test registration with duplicate username."""
        data = {
            'username': 'testuser',
            'email': 'user1@example.com',
            'password': 'password123'
        }

        # First registration
        client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        # Attempt duplicate registration
        data['email'] = 'user2@example.com'
        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400
        json_data = response.get_json()
        assert 'already taken' in json_data['message'].lower()

    def test_register_missing_fields(self, client, mongo):
        """Test registration with missing fields."""
        data = {
            'username': 'newuser'
            # Missing email and password
        }

        response = client.post(
            '/api/auth/register',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_login_success(self, client, mongo):
        """Test successful login."""
        # First register a user
        register_data = {
            'username': 'loginuser',
            'email': 'login@example.com',
            'password': 'password123'
        }

        client.post(
            '/api/auth/register',
            data=json.dumps(register_data),
            content_type='application/json'
        )

        # Now login
        login_data = {
            'email': 'login@example.com',
            'password': 'password123'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['message'] == 'Login successful'
        assert 'token' in json_data
        assert json_data['user']['email'] == 'login@example.com'

    def test_login_invalid_credentials(self, client, mongo):
        """Test login with invalid credentials."""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 401
        json_data = response.get_json()
        assert 'invalid' in json_data['message'].lower()

    def test_login_missing_fields(self, client, mongo):
        """Test login with missing fields."""
        login_data = {
            'email': 'test@example.com'
            # Missing password
        }

        response = client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )

        assert response.status_code == 400
