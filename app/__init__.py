from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register API routes
    from app.routes import api
    api.init_app(app)

    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error"}), 500

    # Catch-all route
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return jsonify({"error": "Invalid route"}), 404

    return app
