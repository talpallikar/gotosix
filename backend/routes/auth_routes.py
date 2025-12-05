from flask import Blueprint, request, jsonify
from bson import ObjectId
from models import User
from auth import hash_password, check_password, generate_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def init_routes(mongo):
    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()

        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing required fields'}), 400

        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'message': 'Email already registered'}), 400

        if mongo.db.users.find_one({'username': data['username']}):
            return jsonify({'message': 'Username already taken'}), 400

        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password'])
        )

        mongo.db.users.insert_one({
            '_id': user._id,
            'username': user.username,
            'email': user.email,
            'password_hash': user.password_hash,
            'created_at': user.created_at
        })

        token = generate_token(user._id)

        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201

    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing email or password'}), 400

        user_data = mongo.db.users.find_one({'email': data['email']})

        if not user_data or not check_password(user_data['password_hash'], data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401

        user = User.from_dict(user_data)
        token = generate_token(user._id)

        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200

    return auth_bp
