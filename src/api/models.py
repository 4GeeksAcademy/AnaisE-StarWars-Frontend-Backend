from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    favorites = relationship('Favorite', back_populates='user')

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
class Character(db.Model):
    __tablename__ = 'character'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    eye_color = Column(String(50))
    gender = Column(String(50))
    hair_color = Column(String(50))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    favorites = relationship('Favorite', back_populates='character')

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
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    diameter = Column(Numeric)
    climate = Column(String(250))
    terrain = Column(String(250))
    created = Column(DateTime, server_default=func.now(), nullable=False)
    edited = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    favorites = relationship('Favorite', back_populates='planet')

def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            ": self,
            
        }

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)
    created = Column(DateTime, server_default=func.now(), nullable=False)
    user = relationship('User', back_populates='favorites')
    character = relationship('Character', back_populates='favorites')
    planet = relationship('Planet', back_populates='favorites')
   