from .main import create_app

__all__ = ['create_app']
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app.config.database import Config

# Initialize extensions
db = SQLAlchemy()

def create_app():
    """Factory function to create Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)  # Enable CORS for all routes
    
    # Import and register blueprints
    from app.routes.news_routes import news_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.prediction_routes import prediction_bp
    
    app.register_blueprint(news_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not create tables: {e}")
    
    return app