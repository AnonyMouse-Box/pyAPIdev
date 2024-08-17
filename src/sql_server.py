#!/usr/bin/env python3


# sql_server.py

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

def init_db(engine):
    Base.metadata.create_all(engine)

def main():
    engine = create_engine("sqlite:///birds.db")
    Session = sessionmaker(bind=engine)
    init_db(engine)

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")