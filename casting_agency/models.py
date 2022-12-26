import os
from sqlalchemy import Column, String, create_engine,DateTime,Da
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

database_path = os.environ["DATABASE_URL"]
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Actor Table:
Have name,gender,date of birth and also actor have nationality.
"""


class Actor(db.Model):
    __tablename__ = "actor"

    id = Column(db.Integer, primary_key=True)
    name = Column(String,nullable=False)
    gender = Column(String,nullable=False)
    date_birth=Column(DateTime,nullable=False)
    nationality=Column(String(length=100),nullable=False)
    performance=db.relationship("Performance",backref="actor",lazy=True)

    def __init__(self, name, gender,date_birth,nationality):
        self.name = name
        self.gender = gender
        self.date_birth=date_birth
        self.nationality=nationality

    def format(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "gender": self.gender,
            "data_birth":self.date_birth,
            "nationality":self.nationality
            }
    def insert(self):
        db.session.add(self)
        db.session.commit() 

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
Movie Type Table
this table will hold the type of movie example "Comdey,Adult,Romance,Avatar,Crime,Action e.t.c"
"""
class MovieType(db.Model):
    __tablename__="movie_type"

    id = Column(db.Integer, primary_key=True)
    type=Column(String(length=50),nullable=False)
    movie=db.relationship("Movie",backref="movie_type",lazy=True)


    def __init__(self,type):
        self.type=type

    def format(self):
        return{
            "id":self.id,
            "type":self.type
        }


    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

"""
Movie Table:
this table has relationship between movie type table becouse every movie has unique type of movie for example "Movie Title: Spiderman, Movie Type: Avatar"
"""

class Movie(db.Model):
    __tablename__="movie"

    id = Column(db.Integer, primary_key=True)
    title=Column(String,nullable=False)
    type_id=Column(db.Integer,db.ForeignKey("movie_type.id"),nullable=False)
    performance=db.relationship("Performance",bacref="movie",lazy=True)

    def __init__(self,title,type_id):
        self.title=title
        self.type_id=type_id

    def format(self):
        return{
            "id":self.id,
            "title":self.title,
            "type_id":self.type_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


"""
Performance:
This Table Has Two Relationship between Actor Table and Movie Table 
"""
class Performance(db.Model):
    __tablename__="performance"

    id = Column(db.Integer, primary_key=True)
    actor_id=Column(db.Integer,db.ForeignKey("actor.id"),nullable=False)
    movie_id=Column(db.Integer,db.ForeignKey("movie.id"),nullable=False)
    release_date=Column(DateTime,server_default=db.func.now(),nullable=False)

    def __init__(self,actor_id,movie_id,release_date):
        self.actor_id=actor_id
        self.movie_id=movie_id
        self.release_date=release_date

    def format(self):
        return{
            "id":self.id,
            "actor_id":self.actor_id,
            "movie_id":self.movie_id,
            "release_date":self.release_date
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
