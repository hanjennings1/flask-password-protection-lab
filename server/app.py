#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')

# Create POST /signup endpoint
class Signup(Resource):
    def post(self):
        json = request.get_json()

        # create user and hash the password:
        user = User(username=json['username'])
        user.password_hash = json['password']

        # queue th enew user & save to db (user gets id)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id # login the user

        return UserSchema().dump(user), 201     # status code for created successfully

api.add_resource(Signup, '/signup', endpoint='signup') # connect Signup to /signup


# Create Login Endpoint
class Login(Resource):

    def post(self):
        json = request.get_json()  # read username and password

        user = User.query.filter(User.username == json['username']).first()  # find user by username

        if user and user.authenticate(json['password']):  # user exists AND password matches
            session['user_id'] = user.id  # log the user in
            return UserSchema().dump(user), 200  # return user as JSON

        return {'error': 'Invalid username or password'}, 401  # login failed

api.add_resource(Login, '/login', endpoint='login')  # connect Login to /login




if __name__ == '__main__':
    app.run(port=5555, debug=True)
