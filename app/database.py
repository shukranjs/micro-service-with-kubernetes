import logging

from flask import Flask, g
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


def init_engine(app: Flask) -> Engine:
    """
    Initializes the SQLAlchemy engine using the database URI from the Flask app
    configuration.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Engine: An SQLAlchemy Engine object.
    """
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    return engine


def init_session(engine: Engine) -> sessionmaker:
    """
    Initializes the SQLAlchemy session factory.

    Args:
        engine (Engine): The SQLAlchemy Engine object.

    Returns:
        sessionmaker: A sessionmaker factory object bound to the provided engine.
    """
    Session = sessionmaker(bind=engine)
    return Session


def init_db(app: Flask) -> sessionmaker:
    """
    Initializes the database by creating all tables and returning a session factory.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        sessionmaker: A sessionmaker factory object that can be used
            to create new sessions.
    """
    engine = init_engine(app)
    Base.metadata.create_all(engine)
    Session = init_session(engine)
    return Session


def get_db(app: Flask) -> Session:
    """
    Retrieves the current database session. If none exists, a new session is created
    and stored in the Flask `g` object.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        Session: An active SQLAlchemy session.
    """
    if "db" not in g:
        # Create a new session and store it in the g object
        g.db = init_db(app)()

    logging.warning(f"Connected to db: {g.db}")
    return g.db


def close_db() -> None:
    """
    Closes the current database session if one exists and removes it
        from the Flask `g` object.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()
    logging.warning("Closed db")
