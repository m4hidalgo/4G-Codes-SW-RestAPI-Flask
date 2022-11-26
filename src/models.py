from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=False)
    mass = db.Column(db.Integer, unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    terrain = db.Column(db.String(120), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
            # do not serialize the password, its a security breach
        }

class Favorite_People(db.Model):
    __tablename__ = 'Favorite_People'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship("User")
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), primary_key=True)
    people = db.relationship("People")
    
    

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id,
            # do not serialize the password, its a security breach
        }


class Favorite_Planet(db.Model):
    __tablename__ = 'Favorite_Planet'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship("User")
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), primary_key=True)
    people = db.relationship("Planet")
    
    

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id
            # do not serialize the password, its a security breach
        }
        