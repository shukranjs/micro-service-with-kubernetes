from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_restx import Api


db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
cache = Cache()
api = Api(
    title="User service",
    version="1.0",
    description="User service",
    doc="/doc",
)
