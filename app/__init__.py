from flask import Flask

from app.config import Config
from app.controllers import Login
from app.database import close_db, get_db
from app.models import Base  # noqa

from .extensions import api, cache, db, jwt, ma, migrate


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
    jwt.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    ma.init_app(app)

    api.init_app(app)

    @app.before_request
    def connect_to_db():
        get_db(app)

    @app.after_request
    def close_db_connection(response):
        close_db()
        return response

    @app.after_request
    def refresh_access_token(response):
        try:
            response = refresh_access_token(response)
            return response
        except (RuntimeError, KeyError):
            return response

    from app.controllers import (HealthCheck, ListCreateUser, RefreshToken,
                                 RetrieveUpdateDeleteUser)

    api.add_resource(HealthCheck, "/health-check")
    api.add_resource(ListCreateUser, "/users")
    api.add_resource(Login, "/login")
    api.add_resource(RefreshToken, "/refresh-token")
    api.add_resource(RetrieveUpdateDeleteUser, "/users/<int:user_id>")
    return app
