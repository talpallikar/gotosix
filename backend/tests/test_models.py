import pytest
from datetime import datetime
from bson import ObjectId
from models import User, Decklist, Scenario, Vote

class TestUserModel:
    def test_user_creation(self):
        """Test creating a user model."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )

        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.password_hash == 'hashed_password'
        assert isinstance(user._id, ObjectId)
        assert isinstance(user.created_at, datetime)

    def test_user_to_dict(self):
        """Test user serialization."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password'
        )

        user_dict = user.to_dict()

        assert user_dict['username'] == 'testuser'
        assert user_dict['email'] == 'test@example.com'
        assert 'password_hash' not in user_dict
        assert '_id' in user_dict
        assert 'created_at' in user_dict

    def test_user_from_dict(self):
        """Test user deserialization."""
        data = {
            '_id': ObjectId(),
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'created_at': datetime.utcnow()
        }

        user = User.from_dict(data)

        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.password_hash == 'hashed_password'

class TestDecklistModel:
    def test_decklist_creation(self):
        """Test creating a decklist model."""
        cards = [
            {'name': 'Lightning Bolt', 'quantity': 4},
            {'name': 'Mountain', 'quantity': 20}
        ]

        decklist = Decklist(
            name='Test Deck',
            format='Modern',
            cards=cards,
            user_id=ObjectId(),
            archetype='Aggro'
        )

        assert decklist.name == 'Test Deck'
        assert decklist.format == 'Modern'
        assert len(decklist.cards) == 2
        assert decklist.archetype == 'Aggro'
        assert decklist.is_public is True

    def test_decklist_to_dict(self):
        """Test decklist serialization."""
        cards = [{'name': 'Lightning Bolt', 'quantity': 4}]
        decklist = Decklist(
            name='Test Deck',
            format='Modern',
            cards=cards,
            user_id=ObjectId()
        )

        decklist_dict = decklist.to_dict()

        assert decklist_dict['name'] == 'Test Deck'
        assert decklist_dict['format'] == 'Modern'
        assert len(decklist_dict['cards']) == 1
        assert decklist_dict['is_public'] is True

class TestScenarioModel:
    def test_scenario_creation(self):
        """Test creating a scenario model."""
        hand = ['Lightning Bolt', 'Mountain', 'Mountain', 'Goblin Guide']

        scenario = Scenario(
            decklist_id=ObjectId(),
            hand=hand,
            on_play=True,
            opponent_archetype='Control',
            game_number=1,
            user_id=ObjectId()
        )

        assert scenario.num_cards == 4
        assert scenario.on_play is True
        assert scenario.opponent_archetype == 'Control'
        assert scenario.game_number == 1
        assert scenario.keep_votes == 0
        assert scenario.mulligan_votes == 0

    def test_scenario_to_dict(self):
        """Test scenario serialization."""
        hand = ['Card 1', 'Card 2']
        scenario = Scenario(
            decklist_id=ObjectId(),
            hand=hand,
            on_play=False,
            opponent_archetype='Aggro',
            game_number=2,
            user_id=ObjectId()
        )

        scenario_dict = scenario.to_dict()

        assert scenario_dict['num_cards'] == 2
        assert scenario_dict['on_play'] is False
        assert scenario_dict['opponent_archetype'] == 'Aggro'
        assert scenario_dict['game_number'] == 2

class TestVoteModel:
    def test_vote_creation(self):
        """Test creating a vote model."""
        vote = Vote(
            scenario_id=ObjectId(),
            user_id=ObjectId(),
            decision='keep'
        )

        assert vote.decision == 'keep'
        assert isinstance(vote._id, ObjectId)
        assert isinstance(vote.created_at, datetime)

    def test_vote_to_dict(self):
        """Test vote serialization."""
        vote = Vote(
            scenario_id=ObjectId(),
            user_id=ObjectId(),
            decision='mulligan'
        )

        vote_dict = vote.to_dict()

        assert vote_dict['decision'] == 'mulligan'
        assert '_id' in vote_dict
        assert 'scenario_id' in vote_dict
        assert 'user_id' in vote_dict
