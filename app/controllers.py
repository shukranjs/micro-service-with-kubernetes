from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, jwt_required)
from flask_restx import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.schemas import UserSchema

from .api_models import login_model, user_model
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

    @jwt_required()
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


class RetrieveUpdateDeleteUser(Resource):
    """
    Resource for retrieving, updating, and deleting a user.
    """

    @jwt_required()
    def get(self, user_id: int) -> tuple[dict, int]:
        """
        Retrieves a user by ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            tuple[dict, int]: A JSON response containing the user data.
        """
        try:
            user = db.session.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}, 404

            return {"success": True, "user": UserSchema().dump(user)}, 200
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    @jwt_required()
    @api.expect(user_model)
    def put(self, user_id: int) -> tuple[dict, int]:
        """
        Updates a user by ID.

        Args:
            user_id (int): The ID of the user to update.

        Returns:
            tuple[dict, int]: A response message with the status code.
        """
        try:
            json_data = request.get_json()
            errors = UserSchema().validate(json_data, partial=True)
            if errors:
                return {"success": False, "errors": errors}, 422

            user = db.session.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}, 404

            user = UserSchema().load(json_data, instance=user, session=db.session)
            user.update_db()
            return {"success": True, "user": UserSchema().dump(user)}, 200
        except ValidationError as e:
            return {"success": False, "errors": e.messages}, 422
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500

    @jwt_required()
    def delete(self, user_id: int) -> tuple[dict, int]:
        """
        Deletes a user by ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            tuple[dict, int]: A response message with the status code.
        """
        try:
            user = db.session.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found"}, 404

            user.delete_from_db()
            return {"success": True, "message": "User deleted"}, 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}, 500
        except Exception as e:
            return {"success": False, "error": str(e)}, 500


class Login(Resource):
    @api.expect(login_model)
    def post(self):
        json_data = request.get_json()
        username = json_data.get("username")
        password = json_data.get("password")

        user = db.session.query(User).filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        response = {
            "success": True,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return response, 200


class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token)
