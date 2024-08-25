from datetime import timedelta
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration settings for the Flask application.
    """

    SECRET_KEY: str = getenv("SECRET_KEY", "my_secret")

    JWT_SECRET_KEY: str = getenv("JWT_SECRET_KEY", "my_jwt_secret")
    JWT_COOKIE_SECURE: bool = True
    JWT_ACCESS_TOKEN_EXPIRES: str = timedelta(hours=1)
    PROPAGATE_EXCEPTIONS: bool = True

    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI")

    DEBUG: bool = True if getenv("FLASK_ENV") == "development" else False
