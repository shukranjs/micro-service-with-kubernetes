from flask import current_app as app
from flask_restx import Resource

from app.database import get_db_session

from .models import User


class HealthCheck(Resource):
    def get(self):
        return {"Ok": True}


class UserOperations(Resource):
    def get(self):
        with get_db_session(app.session) as db:
            users = db.query(User).all()
            return {"users": users}
