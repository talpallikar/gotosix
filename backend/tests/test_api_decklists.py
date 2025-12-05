import pytest
import json
from bson import ObjectId

class TestDecklistAPI:
    def test_create_decklist_success(self, client, mongo, auth_headers):
        """Test successful decklist creation."""
        data = {
            'name': 'Mono Red Aggro',
            'format': 'Modern',
            'archetype': 'Aggro',
            'cards': [
                {'name': 'Lightning Bolt', 'quantity': 4},
                {'name': 'Goblin Guide', 'quantity': 4},
                {'name': 'Mountain', 'quantity': 20}
            ]
        }

        response = client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['message'] == 'Decklist created successfully'
        assert json_data['decklist']['name'] == 'Mono Red Aggro'
        assert json_data['decklist']['format'] == 'Modern'
        assert len(json_data['decklist']['cards']) == 3

    def test_create_decklist_unauthorized(self, client, mongo):
        """Test decklist creation without authentication."""
        data = {
            'name': 'Test Deck',
            'format': 'Modern',
            'cards': []
        }

        response = client.post(
            '/api/decklists',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_create_decklist_missing_fields(self, client, mongo, auth_headers):
        """Test decklist creation with missing fields."""
        data = {
            'name': 'Test Deck'
            # Missing format and cards
        }

        response = client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_get_all_decklists(self, client, mongo, auth_headers):
        """Test retrieving all public decklists."""
        # Create a decklist first
        data = {
            'name': 'Test Deck',
            'format': 'Modern',
            'cards': [{'name': 'Card', 'quantity': 1}]
        }

        client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Get all decklists
        response = client.get('/api/decklists')

        assert response.status_code == 200
        json_data = response.get_json()
        assert 'decklists' in json_data
        assert len(json_data['decklists']) > 0

    def test_get_decklist_by_id(self, client, mongo, auth_headers):
        """Test retrieving a specific decklist by ID."""
        # Create a decklist
        data = {
            'name': 'Specific Deck',
            'format': 'Modern',
            'cards': [{'name': 'Card', 'quantity': 1}]
        }

        create_response = client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        decklist_id = create_response.get_json()['decklist']['_id']

        # Get the decklist
        response = client.get(f'/api/decklists/{decklist_id}')

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['decklist']['name'] == 'Specific Deck'

    def test_get_decklist_invalid_id(self, client, mongo):
        """Test retrieving a decklist with invalid ID."""
        response = client.get('/api/decklists/invalid_id')

        assert response.status_code == 400

    def test_get_decklist_not_found(self, client, mongo):
        """Test retrieving a non-existent decklist."""
        fake_id = str(ObjectId())
        response = client.get(f'/api/decklists/{fake_id}')

        assert response.status_code == 404

    def test_get_my_decklists(self, client, mongo, auth_headers):
        """Test retrieving current user's decklists."""
        # Create a decklist
        data = {
            'name': 'My Deck',
            'format': 'Modern',
            'cards': [{'name': 'Card', 'quantity': 1}]
        }

        client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Get my decklists
        response = client.get('/api/decklists/my', headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert 'decklists' in json_data
        assert len(json_data['decklists']) > 0

    def test_get_my_decklists_unauthorized(self, client, mongo):
        """Test retrieving user's decklists without authentication."""
        response = client.get('/api/decklists/my')

        assert response.status_code == 401
