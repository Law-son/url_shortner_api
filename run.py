import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get debug mode from environment (default: True for development)
    debug_mode = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)
