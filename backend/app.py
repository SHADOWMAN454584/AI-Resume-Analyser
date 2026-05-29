"""
Main application entry point.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    jwt = JWTManager(app)

    # Register blueprints (wrapping inside try-except in case they aren't fully implemented)
    try:
        from routes.auth import auth_bp
        app.register_blueprint(auth_bp)
    except ImportError as e:
        print("Could not import auth_bp:", e)
        
    try:
        from routes.resume import resume_bp
        app.register_blueprint(resume_bp)
    except ImportError as e:
        print("Could not import resume_bp:", e)
        
    try:
        from routes.interview import interview_bp
        app.register_blueprint(interview_bp)
    except ImportError as e:
        print("Could not import interview_bp:", e)
        
    try:
        from routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)
    except ImportError as e:
        print("Could not import dashboard_bp:", e)
        
    try:
        from routes.coding import coding_bp
        app.register_blueprint(coding_bp)
    except ImportError as e:
        print("Could not import coding_bp:", e)

    # Initialize database
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)