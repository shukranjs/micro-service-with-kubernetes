from app.config import Config
from flask import Flask
from flask_restx import Api
from .extensions import db, jwt, migrate, cache


def create_app(config_class: type = Config) -> Api:
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

    api = Api(
        app,
        version="1.0",
        title="User Service",
        description="User service",
    )

    return api
