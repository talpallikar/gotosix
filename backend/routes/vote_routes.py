from flask import Blueprint, request, jsonify
from bson import ObjectId
from models import Vote
from auth import token_required

vote_bp = Blueprint('votes', __name__, url_prefix='/api/votes')

def init_routes(mongo):
    @vote_bp.route('', methods=['POST'])
    @token_required
    def create_vote(user_id):
        data = request.get_json()

        if not data or not data.get('scenario_id') or not data.get('decision'):
            return jsonify({'message': 'Missing required fields'}), 400

        if data['decision'] not in ['keep', 'mulligan']:
            return jsonify({'message': 'Invalid decision (must be "keep" or "mulligan")'}), 400

        try:
            scenario = mongo.db.scenarios.find_one({'_id': ObjectId(data['scenario_id'])})
        except:
            return jsonify({'message': 'Invalid scenario ID'}), 400

        if not scenario:
            return jsonify({'message': 'Scenario not found'}), 404

        existing_vote = mongo.db.votes.find_one({
            'scenario_id': ObjectId(data['scenario_id']),
            'user_id': ObjectId(user_id)
        })

        if existing_vote:
            old_decision = existing_vote['decision']

            mongo.db.votes.update_one(
                {'_id': existing_vote['_id']},
                {'$set': {'decision': data['decision']}}
            )

            if old_decision == 'keep':
                mongo.db.scenarios.update_one(
                    {'_id': ObjectId(data['scenario_id'])},
                    {'$inc': {'keep_votes': -1}}
                )
            else:
                mongo.db.scenarios.update_one(
                    {'_id': ObjectId(data['scenario_id'])},
                    {'$inc': {'mulligan_votes': -1}}
                )

            if data['decision'] == 'keep':
                mongo.db.scenarios.update_one(
                    {'_id': ObjectId(data['scenario_id'])},
                    {'$inc': {'keep_votes': 1}}
                )
            else:
                mongo.db.scenarios.update_one(
                    {'_id': ObjectId(data['scenario_id'])},
                    {'$inc': {'mulligan_votes': 1}}
                )

            return jsonify({'message': 'Vote updated successfully'}), 200

        vote = Vote(
            scenario_id=ObjectId(data['scenario_id']),
            user_id=ObjectId(user_id),
            decision=data['decision']
        )

        mongo.db.votes.insert_one({
            '_id': vote._id,
            'scenario_id': vote.scenario_id,
            'user_id': vote.user_id,
            'decision': vote.decision,
            'created_at': vote.created_at
        })

        if data['decision'] == 'keep':
            mongo.db.scenarios.update_one(
                {'_id': ObjectId(data['scenario_id'])},
                {'$inc': {'keep_votes': 1}}
            )
        else:
            mongo.db.scenarios.update_one(
                {'_id': ObjectId(data['scenario_id'])},
                {'$inc': {'mulligan_votes': 1}}
            )

        return jsonify({
            'message': 'Vote created successfully',
            'vote': vote.to_dict()
        }), 201

    @vote_bp.route('/scenario/<scenario_id>', methods=['GET'])
    @token_required
    def get_user_vote(user_id, scenario_id):
        try:
            vote = mongo.db.votes.find_one({
                'scenario_id': ObjectId(scenario_id),
                'user_id': ObjectId(user_id)
            })
        except:
            return jsonify({'message': 'Invalid scenario ID'}), 400

        if not vote:
            return jsonify({'vote': None}), 200

        vote['_id'] = str(vote['_id'])
        vote['scenario_id'] = str(vote['scenario_id'])
        vote['user_id'] = str(vote['user_id'])
        vote['created_at'] = vote['created_at'].isoformat()

        return jsonify({'vote': vote}), 200

    return vote_bp
