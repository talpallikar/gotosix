import pytest
import json
from bson import ObjectId

class TestVoteAPI:
    @pytest.fixture
    def sample_scenario(self, client, mongo, auth_headers):
        """Create a sample scenario for testing."""
        # First create a decklist
        decklist_data = {
            'name': 'Test Deck',
            'format': 'Modern',
            'cards': [{'name': 'Card', 'quantity': 10}]
        }

        decklist_response = client.post(
            '/api/decklists',
            data=json.dumps(decklist_data),
            headers=auth_headers
        )

        decklist_id = decklist_response.get_json()['decklist']['_id']

        # Create a scenario
        scenario_data = {
            'decklist_id': decklist_id,
            'opponent_archetype': 'Aggro',
            'game_number': 1
        }

        scenario_response = client.post(
            '/api/scenarios',
            data=json.dumps(scenario_data),
            headers=auth_headers
        )

        return scenario_response.get_json()['scenario']['_id']

    def test_create_vote_keep(self, client, mongo, auth_headers, sample_scenario):
        """Test creating a 'keep' vote."""
        data = {
            'scenario_id': sample_scenario,
            'decision': 'keep'
        }

        response = client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['message'] == 'Vote created successfully'
        assert json_data['vote']['decision'] == 'keep'

    def test_create_vote_mulligan(self, client, mongo, auth_headers, sample_scenario):
        """Test creating a 'mulligan' vote."""
        data = {
            'scenario_id': sample_scenario,
            'decision': 'mulligan'
        }

        response = client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.get_json()
        assert json_data['vote']['decision'] == 'mulligan'

    def test_create_vote_unauthorized(self, client, mongo, sample_scenario):
        """Test creating a vote without authentication."""
        data = {
            'scenario_id': sample_scenario,
            'decision': 'keep'
        }

        response = client.post(
            '/api/votes',
            data=json.dumps(data),
            content_type='application/json'
        )

        assert response.status_code == 401

    def test_create_vote_invalid_decision(self, client, mongo, auth_headers, sample_scenario):
        """Test creating a vote with invalid decision."""
        data = {
            'scenario_id': sample_scenario,
            'decision': 'invalid_decision'
        }

        response = client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_update_existing_vote(self, client, mongo, auth_headers, sample_scenario):
        """Test updating an existing vote."""
        # Create initial vote
        data = {
            'scenario_id': sample_scenario,
            'decision': 'keep'
        }

        client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Update vote
        data['decision'] = 'mulligan'
        response = client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['message'] == 'Vote updated successfully'

    def test_get_user_vote(self, client, mongo, auth_headers, sample_scenario):
        """Test retrieving user's vote for a scenario."""
        # Create a vote
        data = {
            'scenario_id': sample_scenario,
            'decision': 'keep'
        }

        client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Get the vote
        response = client.get(
            f'/api/votes/scenario/{sample_scenario}',
            headers=auth_headers
        )

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['vote']['decision'] == 'keep'

    def test_get_user_vote_no_vote(self, client, mongo, auth_headers, sample_scenario):
        """Test retrieving user's vote when no vote exists."""
        response = client.get(
            f'/api/votes/scenario/{sample_scenario}',
            headers=auth_headers
        )

        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['vote'] is None

    def test_get_user_vote_unauthorized(self, client, mongo, sample_scenario):
        """Test retrieving user's vote without authentication."""
        response = client.get(f'/api/votes/scenario/{sample_scenario}')

        assert response.status_code == 401

    def test_vote_increments_scenario_counts(self, client, mongo, auth_headers, sample_scenario):
        """Test that voting increments scenario vote counts."""
        # Vote keep
        data = {
            'scenario_id': sample_scenario,
            'decision': 'keep'
        }

        client.post(
            '/api/votes',
            data=json.dumps(data),
            headers=auth_headers
        )

        # Check scenario has updated count
        response = client.get(f'/api/scenarios/{sample_scenario}')
        scenario = response.get_json()['scenario']

        assert scenario['keep_votes'] == 1
        assert scenario['mulligan_votes'] == 0
