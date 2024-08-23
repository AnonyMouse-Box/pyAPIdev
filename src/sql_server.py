#!/usr/bin/env python3


# sql_server.py

import os, urllib.parse
from sqlalchemy import select, create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class Bird(Base):
    __tablename__ = "bird"
    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    def __repr__(self):
        return f"Bird(id={self.id}, name={self.name!r})"
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

session = None

def init_db():
    username = urllib.parse.quote(os.environ.get("MYSQL_USER"), safe="")
    password = urllib.parse.quote(os.environ.get("DB_PASSWORD"), safe="")
    hostname = urllib.parse.quote(os.environ.get("DB_HOST"), safe="")
    port = urllib.parse.quote(os.environ.get("DB_PORT"), safe="")
    db_name = urllib.parse.quote(os.environ.get("MYSQL_DATABASE"), safe="")
    connection_string = f"mysql+mysqlconnector://{username}:{password}@{hostname}:{port}/{db_name}"
    engine = create_engine(connection_string, echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    global session
    session = Session()

def create_bird(db, bird):
    new_bird = Bird(name=bird["name"])
    db.add(new_bird)
    db.commit()
    db.refresh(new_bird)
    return new_bird

def read_birds(db):
    return db.execute(select(Bird)).scalars().all()

def read_bird(db, bird_id):
    query = select(Bird).where(Bird.id == bird_id)
    return db.execute(query).scalar_one_or_none()

def update_bird(db, bird_id, bird):
    query = select(Bird).where(Bird.id == bird_id)
    bird_found = db.execute(query).scalar_one_or_none()
    if bird_found is not None:
        bird_found.name = bird["name"]
        db.commit()
        db.refresh(bird_found)
    return bird_found

def delete_bird(db, bird_id):
    query = select(Bird).where(Bird.id == bird_id)
    bird_found = db.execute(query).scalar_one_or_none()
    response = {"message": "Item not found."}
    if bird_found is not None:
        db.delete(bird_found)
        db.commit()
        response["message"] = "Bird deleted."
    return response

# Throw an error if run directly.
try:
    assert __name__ != "__main__"
except AssertionError:
    from err import throw
    throw(RuntimeError, "0x02", "Please run from run.py.")