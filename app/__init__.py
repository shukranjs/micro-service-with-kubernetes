from app.config import Config
from flask import Flask
from .extensions import db, jwt, migrate, cache, api
from flask_restx import Resource


def create_app(config_class: type = Config) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_class (type): The configuration class for the Flask app.

    Returns:
        Api: The configured Flask-RESTx Api instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    api.init_app(app)

    return app

@api.route('/home')
class HelloWorld(Resource):
    def get(self):
        return {"hello": "home"}
