from flask import jsonify, request
from flask_restx import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import UserSchema

from .api_models import user_model
from .extensions import api, db
from .models import User


class HealthCheck(Resource):
    """
    A simple health check endpoint.
    """

    def get(self) -> dict:
        """
        Returns a health check response.

        Returns:
            dict: A dictionary indicating the service is healthy.
        """
        try:
            return {"Ok": True}
        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class ListCreateUser(Resource):
    """
    Resource for listing users and creating a new user.
    """

    def get(self) -> jsonify:
        """
        Retrieves a list of users from the database.

        Returns:
            jsonify: A JSON response containing the list of users.
        """
        try:
            users_schema = UserSchema(many=True)
            result = db.session.query(User).all()
            result = users_schema.dump(result)
            return jsonify({"data": result})
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    @api.expect(user_model)
    def post(self) -> tuple[dict, int]:
        """
        Creates a new user based on the provided JSON data.

        Returns:
            tuple[dict, int]: A response message with the status code.
        """
        try:
            json_data = request.get_json()
            errors = UserSchema().validate(json_data)
            if errors:
                return {"success": False, "errors": errors}, 422

            new_user = UserSchema().load(json_data, session=db.session)
            new_user.set_password(json_data["password"])
            new_user.save_to_db()
            return {
                "success": True,
                "user": UserSchema().dump(new_user),
            }, 201
        except ValidationError as e:
            return {"success": False, "errors": e.messages}, 422
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500
