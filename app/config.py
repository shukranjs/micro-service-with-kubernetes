from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration settings for the Flask application.
    """

    SECRET_KEY: str = getenv("SECRET_KEY", "my_secret")

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI: str = getenv("SQLALCHEMY_DATABASE_URI")

    DEBUG: bool = True if getenv("FLASK_ENV") == "development" else False
