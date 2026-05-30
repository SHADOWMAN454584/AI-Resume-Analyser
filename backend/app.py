"""
Main application entry point.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db


def create_app(config_class=Config):
    # In production, serve the frontend build from ../frontend/dist
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
    static_folder = os.path.abspath(static_folder)

    app = Flask(__name__, static_folder=static_folder, static_url_path='')
    app.config.from_object(config_class)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})
    jwt = JWTManager(app)

    # Register blueprints
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
        from routes.dashboard import dashboard_bp
        app.register_blueprint(dashboard_bp)
    except ImportError as e:
        print("Could not import dashboard_bp:", e)

    # Initialize database
    with app.app_context():
        db.create_all()

    # ── Serve React frontend ──────────────────────────────────
    # Serve index.html for the root and any non-API routes (SPA fallback)
    @app.route('/')
    @app.route('/<path:path>')
    def serve_frontend(path=''):
        # If the path matches an actual file in dist/, serve it
        file_path = os.path.join(static_folder, path)
        if path and os.path.isfile(file_path):
            return send_from_directory(static_folder, path)
        # Otherwise serve index.html for client-side routing
        index_path = os.path.join(static_folder, 'index.html')
        if os.path.isfile(index_path):
            return send_from_directory(static_folder, 'index.html')
        # If no frontend build exists, return a simple message
        return '<h1>ResumeAI API is running</h1><p>Frontend not built yet. Run <code>npm run build</code> in /frontend.</p>', 200

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)