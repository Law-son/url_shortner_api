from flask import request, jsonify
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from app import db
from app.models import User
from config import Config
from app.utils import generate_jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 401
        try:
            token = token.split()[1]  # Bearer <token>
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except Exception:
            return {'message': 'Token is invalid or expired!'}, 401
        return f(current_user, *args, **kwargs)
    return decorated

class UserRegister(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password are required!'}, 400

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(email=data['email'], password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully!'}, 201
        except Exception:
            return {'message': 'User already exists or other error!'}, 400

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return {'message': 'Email and password are required!'}, 400

        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid email or password!'}, 401

        token = generate_jwt(user.id)
        return {'token': token}, 200

