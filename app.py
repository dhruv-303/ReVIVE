import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS for Vite React dev server and production origins
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Register all modular blueprints
    register_blueprints(app)

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'online',
            'project': 'ReVive Refurbished Marketplace API',
            'version': '2.0.0',
            'database_uri': app.config['SQLALCHEMY_DATABASE_URI'].split('@')[-1] if '@' in app.config['SQLALCHEMY_DATABASE_URI'] else 'sqlite local',
            'database_type': getattr(Config, 'ACTIVE_DB_TYPE', 'Configured')
        }), 200

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("🚀 ReVive Database tables verified and created successfully.")
            # Run automatic seed if database has no categories
            from seed import seed_database
            seed_database()
        except Exception as e:
            print(f"⚠️ Notice on database initialization: {e}")

    port = int(os.environ.get('PORT', 5000))
    print(f"============================================================")
    print(f"  ReVive Refurbished Marketplace Backend API")
    print(f"  Listening on: http://127.0.0.1:{port}")
    print(f"  Active Database: {getattr(Config, 'ACTIVE_DB_TYPE', 'Configured')}")
    print(f"============================================================")
    app.run(host='0.0.0.0', port=port, debug=True)

