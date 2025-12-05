from flask import Blueprint, request, jsonify
from bson import ObjectId
import random
from models import Scenario
from auth import token_required

scenario_bp = Blueprint('scenarios', __name__, url_prefix='/api/scenarios')

def init_routes(mongo):
    @scenario_bp.route('', methods=['POST'])
    @token_required
    def create_scenario(user_id):
        data = request.get_json()

        if not data or not data.get('decklist_id') or not data.get('opponent_archetype') or 'game_number' not in data:
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            decklist = mongo.db.decklists.find_one({'_id': ObjectId(data['decklist_id'])})
        except:
            return jsonify({'message': 'Invalid decklist ID'}), 400

        if not decklist:
            return jsonify({'message': 'Decklist not found'}), 404

        num_cards = data.get('num_cards', 7)
        if num_cards < 0 or num_cards > 7:
            return jsonify({'message': 'Invalid number of cards (must be 0-7)'}), 400

        hand = generate_hand(decklist['cards'], num_cards)

        scenario = Scenario(
            decklist_id=ObjectId(data['decklist_id']),
            hand=hand,
            on_play=data.get('on_play', True),
            opponent_archetype=data['opponent_archetype'],
            game_number=data['game_number'],
            user_id=ObjectId(user_id)
        )

        mongo.db.scenarios.insert_one({
            '_id': scenario._id,
            'decklist_id': scenario.decklist_id,
            'hand': scenario.hand,
            'num_cards': scenario.num_cards,
            'on_play': scenario.on_play,
            'opponent_archetype': scenario.opponent_archetype,
            'game_number': scenario.game_number,
            'user_id': scenario.user_id,
            'created_at': scenario.created_at,
            'keep_votes': scenario.keep_votes,
            'mulligan_votes': scenario.mulligan_votes
        })

        return jsonify({
            'message': 'Scenario created successfully',
            'scenario': scenario.to_dict()
        }), 201

    @scenario_bp.route('', methods=['GET'])
    def get_scenarios():
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        skip = (page - 1) * per_page

        scenarios = list(mongo.db.scenarios.find().sort('created_at', -1).skip(skip).limit(per_page))

        for scenario in scenarios:
            scenario['_id'] = str(scenario['_id'])
            scenario['decklist_id'] = str(scenario['decklist_id'])
            scenario['user_id'] = str(scenario['user_id'])
            scenario['created_at'] = scenario['created_at'].isoformat()

        total = mongo.db.scenarios.count_documents({})

        return jsonify({
            'scenarios': scenarios,
            'total': total,
            'page': page,
            'per_page': per_page
        }), 200

    @scenario_bp.route('/<scenario_id>', methods=['GET'])
    def get_scenario(scenario_id):
        try:
            scenario = mongo.db.scenarios.find_one({'_id': ObjectId(scenario_id)})
        except:
            return jsonify({'message': 'Invalid scenario ID'}), 400

        if not scenario:
            return jsonify({'message': 'Scenario not found'}), 404

        decklist = mongo.db.decklists.find_one({'_id': scenario['decklist_id']})

        scenario['_id'] = str(scenario['_id'])
        scenario['decklist_id'] = str(scenario['decklist_id'])
        scenario['user_id'] = str(scenario['user_id'])
        scenario['created_at'] = scenario['created_at'].isoformat()

        if decklist:
            decklist['_id'] = str(decklist['_id'])
            decklist['user_id'] = str(decklist['user_id'])
            decklist['created_at'] = decklist['created_at'].isoformat()
            scenario['decklist'] = decklist

        return jsonify({'scenario': scenario}), 200

    return scenario_bp

def generate_hand(cards, num_cards):
    deck = []
    for card in cards:
        deck.extend([card['name']] * card['quantity'])

    if len(deck) < num_cards:
        return random.sample(deck, len(deck))

    return random.sample(deck, num_cards)
