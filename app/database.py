from contextlib import contextmanager

from flask import Flask
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


@contextmanager
def get_db_session(Session):
    session = Session()
    try:
        yield session
    finally:
        session.close()


def init_db(app: Flask):
    engine = init_engine(app)
    Base.metadata.create_all(engine)
    return init_session(engine)
