from flask import request, jsonify
from flask_restful import Resource, reqparse
from app import db
from app.models import User
from app.utils import generate_jwt
from config import Config
from functools import wraps
import jwt

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
            if not current_user:
                return {'message': 'User not found!'}, 404
        except jwt.ExpiredSignatureError:
            return {'message': 'Token has expired!'}, 401
        except jwt.InvalidTokenError:
            return {'message': 'Invalid token!'}, 401
        except Exception as e:
            return {'message': f"An unexpected error occurred: {str(e)}"}, 500
        return f(current_user, *args, **kwargs)
    return decorated

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email is required")
        parser.add_argument('password', type=str, required=True, help="Password is required")
        data = parser.parse_args()

        try:
            # Check if user already exists
            if User.query.filter_by(email=data['email']).first():
                return {"message": "User already exists"}, 400

            # Create new user
            new_user = User(email=data['email'])
            new_user.password = data['password']

            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creating user: {str(e)}"}, 500

class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or not data.get('email') or not data.get('password'):
                return {'message': 'Email and password are required!'}, 400

            user = User.query.filter_by(email=data['email']).first()
            if not user or not user.check_password(data['password']):
                return {'message': 'Invalid email or password!'}, 401

            token = generate_jwt(user.id)
            return {'token': token}, 200

        except jwt.PyJWTError as jwt_error:
            return {"message": f"Token generation error: {str(jwt_error)}"}, 500
        except Exception as e:
            return {"message": f"An unexpected error occurred: {str(e)}"}, 500
