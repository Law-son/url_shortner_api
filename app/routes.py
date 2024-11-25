from flask import request, jsonify, redirect
from flask_restful import Api, Resource
from app import db
from app.models import URL, Visit
from app.utils import generate_short_url
from app.auth import UserRegister, UserLogin, token_required

api = Api()

class HelloWorld(Resource):
    def get(self):
        """Returns a simple 'Hello, World!' message"""
        return {'message': 'Hello, World!'}

class ShortenURL(Resource):
    @token_required
    def post(self, current_user):
        """Handles the shortening of a URL"""
        # print(f"DEBUG: Current user: {current_user}, Type: {type(current_user)}")
        data = request.get_json()  # Ensures valid JSON data
        original_url = data.get('original_url')
        
        if not original_url:
            return {'error': 'Original URL is required'}, 400

        # Check if the URL already exists for this user
        existing_url = URL.query.filter_by(original_url=original_url, user_id=current_user.id).first()
        if existing_url:
            return {'short_url': existing_url.short_url}, 200

        # Generate a unique short URL
        short_url = generate_short_url(original_url=original_url)
        new_url = URL(
            original_url=original_url,
            short_url=short_url,
            user_id=current_user.id  # Associate URL with the current user
        )
        db.session.add(new_url)
        db.session.commit()
        
        return {'short_url': short_url}, 201


class RedirectURL(Resource):
    def get(self, short_url):
        """Handles redirection from short URL to original URL"""
        url = URL.query.filter_by(short_url=short_url).first()
        if not url:
            return {'error': 'URL not found'}, 404

        # Track visit details
        visit = Visit(
            user_agent=request.headers.get('User-Agent', 'Unknown'),
            ip_address=request.remote_addr or 'Unknown',
            url_id=url.id
        )
        db.session.add(visit)
        db.session.commit()

        return redirect(url.original_url)


class Analytics(Resource):
    @token_required
    def get(self, current_user, short_url):
        """Fetches analytics for a specific short URL owned by the current user."""
        # Filter by both the short_url and the current_user's ID
        url = URL.query.filter_by(short_url=short_url, user_id=current_user.id).first()
        
        if not url:
            return {'error': 'URL not found or access denied'}, 404

        # Build analytics response
        analytics = {
            'total_visits': len(url.visits),
            'visits': [
                {
                    'timestamp': visit.timestamp.isoformat(),
                    'ip_address': visit.ip_address,
                    'user_agent': visit.user_agent
                } for visit in url.visits
            ]
        }
        return analytics, 200


# Register resources with the Flask-RESTful API
api.add_resource(HelloWorld, '/')
api.add_resource(ShortenURL, '/shorten')
api.add_resource(RedirectURL, '/<string:short_url>')
api.add_resource(Analytics, '/<string:short_url>/analytics')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')

