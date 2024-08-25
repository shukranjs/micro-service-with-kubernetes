from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

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

ma = Marshmallow()
