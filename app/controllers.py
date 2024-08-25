from flask_restx import Resource


class HealthCheck(Resource):
    def get(self):
        return {"Ok": True}


class UserOperations(Resource):
    def get(self):
        return {"Ok": True}
