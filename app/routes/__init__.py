from .auth_routes import auth_bp
from .news_routes import news_bp
from .prediction_routes import prediction_bp

__all__ = ['auth_bp', 'news_bp', 'prediction_bp']