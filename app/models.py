from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db  # Use the centralized db instance

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    urls = db.relationship('URL', backref='user', lazy=True)

    # Password setter
    @property
    def password(self):
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def __repr__(self):
        return f"<User {self.email}>"

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_url = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    visits = db.relationship('Visit', backref='url', lazy=True)

    def __repr__(self):
        return f"<URL {self.short_url}>"

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(256))
    ip_address = db.Column(db.String(45))
    url_id = db.Column(db.Integer, db.ForeignKey('url.id'), nullable=False)

    def __repr__(self):
        return f"<Visit {self.id} on URL {self.url_id}>"
