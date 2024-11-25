import jwt
import datetime
from config import Config
import hashlib
import random
import string

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


def generate_short_url(original_url=None):
    """
    Generates a unique short URL string in the format of any 6 random string
    characters, a dot, and then 'nib'.
    
    :param original_url: (Optional) The original URL to base the hash on.
                         If None, a random string is used.
    :return: A short string (e.g., 'abcdef.nib') representing the short URL.
    """
    if original_url:
        # Use a hash of the original URL for repeatability
        hashed = hashlib.md5(original_url.encode()).hexdigest()
        return hashed[:6] + '.nib'  # Use the first 6 characters of the hash
    else:
        # Generate a random string if no URL is provided
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '.nib'


