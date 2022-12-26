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
    date_birth=Column(datetime.date,nullable=False)
    nationality=Column(String(length=100),nullable=False)

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
Movie Type
this table will hold the type of movie example "Comdey,Adult,Romance,Avatar,Crime,Action e.t.c"
"""
class MovieType(db.Model):
    __tablename__="movie_type"

    id=Column(db.Integer, primary_key=True)
    type=Column(String(length=50),nullable=False)


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
"""