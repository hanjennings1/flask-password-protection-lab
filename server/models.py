from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields

from config import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)

    # protect the password_property by raising an Exception
    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')


    # Build method to set password hash property using bcrypt.generate_password_hash()
    @password_hash.setter
    def password_hash(self, password):
        pass

    # Build authenticate method that uses bcrypt.check_password_hash()
    def authenticate(self, password):
        pass

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'

class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()