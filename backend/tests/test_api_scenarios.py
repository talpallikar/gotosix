import pytest
import json
from bson import ObjectId

class TestScenarioAPI:
    @pytest.fixture
    def sample_decklist(self, client, mongo, auth_headers):
        """Create a sample decklist for testing."""
        data = {
            'name': 'Test Deck',
            'format': 'Modern',
            'cards': [
                {'name': 'Lightning Bolt', 'quantity': 4},
                {'name': 'Mountain', 'quantity': 20}
            ]
        }

        response = client.post(
            '/api/decklists',
            data=json.dumps(data),
            headers=auth_headers
        )

        return response.get_json()['decklist']['_id']

    def test_create_scenario_success(self, client, mongo, auth_headers, sample_decklist):
        """Test successful scenario creation."""
        data = {
            'decklist_id': sample_decklist,
            'num_cards': 7,
            'on_play': True,
            'opponent_archetype': 'Control',
            'game_number': 1
        }

        response = client.post(
            '/api/scenarios',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['message'] == 'Scenario created successfully'
        assert json_data['scenario']['num_cards'] == 7
        assert json_data['scenario']['on_play'] is True
        assert len(json_data['scenario']['hand']) == 7

    def test_create_scenario_unauthorized(self, client, mongo, sample_decklist):
        """Test scenario creation without authentication."""
        data = {
            'decklist_id': sample_decklist,
            'opponent_archetype': 'Aggro',
            'game_number': 1
        }

        response = client.post(
            '/api/scenarios',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_create_scenario_invalid_decklist(self, client, mongo, auth_headers):
        """Test scenario creation with invalid decklist ID."""
        data = {
            'decklist_id': 'invalid_id',
            'opponent_archetype': 'Control',
            'game_number': 1
        }

        response = client.post(
            '/api/scenarios',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_create_scenario_missing_fields(self, client, mongo, auth_headers, sample_decklist):
        """Test scenario creation with missing fields."""
        data = {
            'decklist_id': sample_decklist
            # Missing opponent_archetype and game_number
        }

        response = client.post(
            '/api/scenarios',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_get_all_scenarios(self, client, mongo, auth_headers, sample_decklist):
        """Test retrieving all scenarios."""
        # Create a scenario first
        data = {
            'decklist_id': sample_decklist,
            'opponent_archetype': 'Aggro',
            'game_number': 1
        }

        client.post(
            '/api/scenarios',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Get all scenarios
        response = client.get('/api/scenarios')

        assert response.status_code == 200
        json_data = response.get_json()
        assert 'scenarios' in json_data
        assert 'total' in json_data
        assert 'page' in json_data

    def test_get_scenarios_pagination(self, client, mongo):
        """Test scenario pagination."""
        response = client.get('/api/scenarios?page=1&per_page=10')

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['page'] == 1
        assert json_data['per_page'] == 10

    def test_get_scenario_by_id(self, client, mongo, auth_headers, sample_decklist):
        """Test retrieving a specific scenario."""
        # Create a scenario
        data = {
            'decklist_id': sample_decklist,
            'opponent_archetype': 'Control',
            'game_number': 2
        }

        create_response = client.post(
            '/api/scenarios',
            data=json.dumps(data),
            headers=auth_headers
        )

        scenario_id = create_response.get_json()['scenario']['_id']

        # Get the scenario
        response = client.get(f'/api/scenarios/{scenario_id}')

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['scenario']['opponent_archetype'] == 'Control'
        assert 'decklist' in json_data['scenario']

    def test_get_scenario_not_found(self, client, mongo):
        """Test retrieving a non-existent scenario."""
        fake_id = str(ObjectId())
        response = client.get(f'/api/scenarios/{fake_id}')

        assert response.status_code == 404
