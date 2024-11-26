from flask import request, jsonify
from flask_restful import Resource, reqparse
from app import db
from app.models import User
from app.utils import generate_jwt
from config import Config
from functools import wraps
import jwt
import re
from passlib.hash import bcrypt
from validators import email as validate_email

def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
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
        
        # Pass self explicitly as the first argument
        return f(self, current_user, *args, **kwargs)
    return decorated


class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help="Email is required")
        parser.add_argument('password', type=str, required=True, help="Password is required")
        data = parser.parse_args()

        email = data['email']
        password = data['password']

        # Validate email
        if not validate_email(email):
            return {"message": "Invalid email format"}, 400

        # Validate password strength
        if not self.is_strong_password(password):
            return {
                "message": "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character"
            }, 400

        try:
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                return {"message": "User already exists"}, 400

            # Create new user
            new_user = User(email=email)
            new_user.password = password  # The model will hash the password automatically

            db.session.add(new_user)
            db.session.commit()
            return {"message": "User created successfully"}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": f"Error creating user: {str(e)}"}, 500

    @staticmethod
    def is_strong_password(password):
        """Check if the password is strong."""
        if (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and  # At least one uppercase letter
            re.search(r'[a-z]', password) and  # At least one lowercase letter
            re.search(r'[0-9]', password) and  # At least one digit
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # At least one special character
        ):
            return True
        return False


    @staticmethod
    def is_strong_password(password):
        """Check if the password is strong."""
        if (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and  # At least one uppercase letter
            re.search(r'[a-z]', password) and  # At least one lowercase letter
            re.search(r'[0-9]', password) and  # At least one digit
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)  # At least one special character
        ):
            return True
        return False

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