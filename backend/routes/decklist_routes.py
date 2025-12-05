from flask import Blueprint, request, jsonify
from bson import ObjectId
from models import Decklist
from auth import token_required

decklist_bp = Blueprint('decklists', __name__, url_prefix='/api/decklists')

def init_routes(mongo):
    @decklist_bp.route('', methods=['POST'])
    @token_required
    def create_decklist(user_id):
        data = request.get_json()

        if not data or not data.get('name') or not data.get('format') or not data.get('cards'):
            return jsonify({'message': 'Missing required fields'}), 400

        decklist = Decklist(
            name=data['name'],
            format=data['format'],
            cards=data['cards'],
            user_id=ObjectId(user_id),
            archetype=data.get('archetype')
        )

        result = mongo.db.decklists.insert_one({
            '_id': decklist._id,
            'name': decklist.name,
            'format': decklist.format,
            'cards': decklist.cards,
            'user_id': decklist.user_id,
            'archetype': decklist.archetype,
            'created_at': decklist.created_at,
            'is_public': decklist.is_public
        })

        return jsonify({
            'message': 'Decklist created successfully',
            'decklist': decklist.to_dict()
        }), 201

    @decklist_bp.route('', methods=['GET'])
    def get_decklists():
        decklists = list(mongo.db.decklists.find({'is_public': True}).sort('created_at', -1).limit(50))

        for decklist in decklists:
            decklist['_id'] = str(decklist['_id'])
            decklist['user_id'] = str(decklist['user_id'])
            decklist['created_at'] = decklist['created_at'].isoformat()

        return jsonify({'decklists': decklists}), 200

    @decklist_bp.route('/<decklist_id>', methods=['GET'])
    def get_decklist(decklist_id):
        try:
            decklist = mongo.db.decklists.find_one({'_id': ObjectId(decklist_id)})
        except:
            return jsonify({'message': 'Invalid decklist ID'}), 400

        if not decklist:
            return jsonify({'message': 'Decklist not found'}), 404

        decklist['_id'] = str(decklist['_id'])
        decklist['user_id'] = str(decklist['user_id'])
        decklist['created_at'] = decklist['created_at'].isoformat()

        return jsonify({'decklist': decklist}), 200

    @decklist_bp.route('/my', methods=['GET'])
    @token_required
    def get_my_decklists(user_id):
        decklists = list(mongo.db.decklists.find({'user_id': ObjectId(user_id)}).sort('created_at', -1))

        for decklist in decklists:
            decklist['_id'] = str(decklist['_id'])
            decklist['user_id'] = str(decklist['user_id'])
            decklist['created_at'] = decklist['created_at'].isoformat()

        return jsonify({'decklists': decklists}), 200

    return decklist_bp
