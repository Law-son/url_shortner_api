from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from app import db
from app.models import User
from config import Config
from app.utils import generate_jwt

auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            token = token.split()[1]
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except Exception:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception:
        return jsonify({'message': 'User already exists or other error!'}), 400

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required!'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password!'}), 401

    token = generate_jwt(user.id)
    return jsonify({'token': token}), 200


@auth.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({
        'message': 'This is a protected route.',
        'user': current_user.username
    }), 200
