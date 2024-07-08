import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    # db.drop_all()
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    # Auto incrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String Title
    title = Column(String(), nullable=False)
    # Integer release_year
    release_year = Column(Integer(), nullable=False)
    # Create a relationship
    actors = db.relationship('Actor', backref='movies')

    # insert to database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update to database
    def update(self):
        db.session.commit()

    # delete to database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #format output
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    # Auto incrementing, unique primary key
    id = Column(Integer(), primary_key=True)
    # String name
    name = Column(String(), nullable=False)
    # Integer age
    age = Column(Integer(), nullable=False)
    # String gender
    gender = Column(String(), nullable=False)
    # Integer movie_id
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    # insert to database
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # update to database
    def update(self):
        db.session.commit()

    # delete to database
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    #format output
    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
