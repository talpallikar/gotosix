from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from config import config
import os

from routes.auth_routes import init_routes as init_auth_routes
from routes.decklist_routes import init_routes as init_decklist_routes
from routes.scenario_routes import init_routes as init_scenario_routes
from routes.vote_routes import init_routes as init_vote_routes

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config[config_name])

    CORS(app)

    mongo = PyMongo(app)

    auth_bp = init_auth_routes(mongo)
    decklist_bp = init_decklist_routes(mongo)
    scenario_bp = init_scenario_routes(mongo)
    vote_bp = init_vote_routes(mongo)

    app.register_blueprint(auth_bp)
    app.register_blueprint(decklist_bp)
    app.register_blueprint(scenario_bp)
    app.register_blueprint(vote_bp)

    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'healthy'}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
