import jwt
import datetime
from config import Config
import string
import random

def generate_jwt(user_id):
    """Generate a JWT token for the given user ID."""
    token = jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    return token


