from flask import Flask

from app.config import Config
from app.database import init_db
from app.models import Base  # noqa

from .extensions import api, cache, db, jwt, migrate


def create_app(config_class: type = Config) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_class (type): The configuration class for the Flask app.

    Returns:
        Flask: The configured Flask instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    session = init_db(app)
    app.session = session
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    api.init_app(app)

    from app.controllers import HealthCheck, UserOperations

    api.add_resource(HealthCheck, "/health-check")
    api.add_resource(UserOperations, "/users")

    return app
