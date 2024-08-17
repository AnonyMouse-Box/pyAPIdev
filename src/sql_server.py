#!/usr/bin/env python3


# sql_server.py

import os, urllib.parse
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class Bird(Base):
    __tablename__ = "bird"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Bird(id={self.id}, name={self.name!r})"

username = urllib.parse.quote(os.environ.get("MYSQL_USER"), safe="")
password = urllib.parse.quote(os.environ.get("DB_PASSWORD"), safe="")
hostname = urllib.parse.quote(os.environ.get("DB_HOST"), safe="")
port = urllib.parse.quote(os.environ.get("DB_PORT"), safe="")
db_name = urllib.parse.quote(os.environ.get("MYSQL_DATABASE"), safe="")
connection_string = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{db_name}"
engine = create_engine(connection_string, echo=True)
session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

def main():
    init_db()
    new_bird = Bird(name="Test Bird")
    session.add(new_bird)
    session.commit()

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")