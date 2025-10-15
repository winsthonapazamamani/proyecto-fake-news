from flask import Flask
from flask_cors import CORS
from config.database import init_db
from routes.auth_routes import auth_bp
from routes.news_routes import news_bp
from routes.prediction_routes import prediction_bp
import os
from utils.logger import setup_logger

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_SORT_KEYS'] = False
    
    # CORS
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Base de datos
    init_db(app)
    
    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
    
    # Logger
    setup_logger()
    
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'message': 'News Prediction API is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)