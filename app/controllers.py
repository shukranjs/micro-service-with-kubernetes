from flask import jsonify, request
from flask_restx import Resource, fields

from app.schemas import UserSchema

from .extensions import api, db
from .models import User


class HealthCheck(Resource):
    def get(self):
        return {"Ok": True}


user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
        ),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "username": fields.String(required=True, description="Username of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="Password of the user"),
    },
)

user_schema = UserSchema()


class ListCreateUser(Resource):
    def get(self):
        users_schema = UserSchema(many=True)
        result = db.session.query(User).all()
        result = users_schema.dump(result)
        return jsonify({"data": result})

    @api.expect(user_model)
    def post(self):
        json_data = request.get_json()
        errors = user_schema.validate(json_data)
        if errors:
            return errors, 422

        new_user = user_schema.load(json_data, session=db.session)
        new_user.save_to_db()
        # db.session.add(new_user)
        # db.session.commit()

        return {
            "message": "User created successfully",
            "user": user_schema.dump(new_user),
        }, 201
