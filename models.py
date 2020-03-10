import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_test_data()

# '''
# db_test_data()
#     sample data for testing
# '''
def db_test_data():
    actor1 = (Actor(
        name='Will Smith',
        gender='Male',
        age=51
        ))
    actor1.insert()

    actor2 = (Actor(
        name='Margot Robbie',
        gender='Female',
        age=29
        ))
    actor2.insert()

    movie1 = (Movie(
        title='The Pursuit of Happiness',
        year=2006,
        ))
    movie1.insert()

    movie2 = (Movie(
        title='Suicide Squad',
        year=2016,
        ))
    movie2.insert()

    
'''
Actor
'''
class Actor(db.Model):  
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }

'''
Movie
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)

    def __init__(self, title, year):
        self.title = title
        self.year = year

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year
        }