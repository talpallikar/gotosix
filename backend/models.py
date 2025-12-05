from datetime import datetime
from bson import ObjectId

class User:
    def __init__(self, username, email, password_hash, _id=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            _id=data.get('_id')
        )
        if 'created_at' in data:
            user.created_at = data['created_at']
        return user

class Decklist:
    def __init__(self, name, format, cards, user_id, archetype=None, _id=None):
        self.name = name
        self.format = format
        self.cards = cards  # List of {name: str, quantity: int}
        self.user_id = user_id
        self.archetype = archetype
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()
        self.is_public = True

    def to_dict(self):
        return {
            '_id': str(self._id),
            'name': self.name,
            'format': self.format,
            'cards': self.cards,
            'user_id': str(self.user_id),
            'archetype': self.archetype,
            'created_at': self.created_at.isoformat(),
            'is_public': self.is_public
        }

class Scenario:
    def __init__(self, decklist_id, hand, on_play, opponent_archetype, game_number, user_id, mulligan_count=0, _id=None):
        self.decklist_id = decklist_id
        self.hand = hand  # Always 7 cards for London Mulligan
        self.mulligan_count = mulligan_count  # How many times mulliganed (0-6)
        self.num_cards = 7 - mulligan_count  # Final hand size after bottoming
        self.on_play = on_play  # True if on the play, False if on the draw
        self.opponent_archetype = opponent_archetype
        self.game_number = game_number  # 1, 2, or 3
        self.user_id = user_id
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()
        self.keep_votes = 0
        self.mulligan_votes = 0

    def to_dict(self):
        return {
            '_id': str(self._id),
            'decklist_id': str(self.decklist_id),
            'hand': self.hand,
            'mulligan_count': self.mulligan_count,
            'num_cards': self.num_cards,
            'on_play': self.on_play,
            'opponent_archetype': self.opponent_archetype,
            'game_number': self.game_number,
            'user_id': str(self.user_id),
            'created_at': self.created_at.isoformat(),
            'keep_votes': self.keep_votes,
            'mulligan_votes': self.mulligan_votes
        }

class Vote:
    def __init__(self, scenario_id, user_id, decision, _id=None):
        self.scenario_id = scenario_id
        self.user_id = user_id
        self.decision = decision  # 'keep' or 'mulligan'
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()

    def to_dict(self):
        return {
            '_id': str(self._id),
            'scenario_id': str(self.scenario_id),
            'user_id': str(self.user_id),
            'decision': self.decision,
            'created_at': self.created_at.isoformat()
        }
