import logging

from flask import Flask, g
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


def init_engine(app: Flask):
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    return engine


def init_session(engine):
    Session = sessionmaker(bind=engine)
    return Session


def init_db(app: Flask):
    engine = init_engine(app)
    Base.metadata.create_all(engine)
    Session = init_session(engine)
    return Session


def get_db(app):
    if "db" not in g:
        # Create a new session and store it in the g object
        g.db = init_db(app)()

    logging.warning(f"Connected to db: {g.db}")
    return g.db


def close_db():
    db = g.pop("db", None)

    if db is not None:
        db.close()
    logging.warning("Closed db")
