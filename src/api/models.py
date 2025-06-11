from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import ARRAY, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    favorite_characters = relationship('FavoriteCharacter', back_populates='user')
    favorite_planets = relationship('FavoritePlanet', back_populates='user')

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "created": self.created,
            "edited": self.edited
            # do not serialize the password, its a security breach
        }
    def serialize_favorites(self):
        return {
            "characters": [favorite.serialize() for favorite in self.favorite_characters] if len(self.favorite_characters) > 0 else [],
            "planets": [favorite.serialize() for favorite in self.favorite_planets] if len(self.favorite_planets) > 0 else []
        }
class Character(db.Model):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    eye_color = Column(String(50))
    gender = Column(String(50))
    hair_color = Column(String(50))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    favorites = relationship('FavoriteCharacter', back_populates='character')

    def __repr__(self):
        return f'<Character {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "created": self.created,
            "edited": self.edited,
                    
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    diameter = Column(Numeric)
    climate = Column(String(250))
    terrain = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    favorites = relationship('FavoritePlanet', back_populates='planet')

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "created": self.created,
            "edited": self.edited,
            
        }

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    user = relationship('User')
    character = relationship('Character')
    
    def __repr__(self):
        return f'<FavoriteCharacter {self.character.name}>'

    def serialize(self):
        return self.character.serialize()
        
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planets.id'), nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    user = relationship('User')
    planet = relationship('Planet')
    
    def __repr__(self):
        return f'<FavoritePlanet {self.planet.name}>'

    def serialize(self):
        return self.planet.serialize()