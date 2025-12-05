import pytest
from auth import hash_password, check_password, generate_token, decode_token

class TestAuth:
    def test_hash_password(self):
        """Test password hashing."""
        password = 'test_password_123'
        hashed = hash_password(password)

        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 0

    def test_check_password_correct(self):
        """Test password verification with correct password."""
        password = 'test_password_123'
        hashed = hash_password(password)

        assert check_password(hashed, password) is True

    def test_check_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = 'test_password_123'
        hashed = hash_password(password)

        assert check_password(hashed, 'wrong_password') is False

    def test_generate_token(self, app):
        """Test JWT token generation."""
        with app.app_context():
            from bson import ObjectId
            user_id = ObjectId()
            token = generate_token(user_id)

            assert token is not None
            assert isinstance(token, str)
            assert len(token) > 0

    def test_decode_token_valid(self, app):
        """Test decoding a valid token."""
        with app.app_context():
            from bson import ObjectId
            user_id = ObjectId()
            token = generate_token(user_id)
            decoded_id = decode_token(token)

            assert decoded_id == str(user_id)

    def test_decode_token_invalid(self, app):
        """Test decoding an invalid token."""
        with app.app_context():
            result = decode_token('invalid_token')
            assert result is None
