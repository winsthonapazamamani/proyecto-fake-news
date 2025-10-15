from flask import Blueprint
from app.controllers.news_controller import NewsController

news_bp = Blueprint('news', __name__)

@news_bp.route('/api/news/verifications', methods=['GET'])
def get_verifications():
    return NewsController.get_verifications()

@news_bp.route('/api/news/verifications/<int:verification_id>', methods=['GET'])
def get_verification(verification_id):
    return NewsController.get_verification(verification_id)

@news_bp.route('/api/news/articles', methods=['POST'])
def create_article():
    return NewsController.create_article()

@news_bp.route('/api/news/articles', methods=['GET'])
def get_articles():
    return NewsController.get_articles()

@news_bp.route('/api/news/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    return NewsController.get_article(article_id)

@news_bp.route('/api/news/categories', methods=['GET'])
def get_categories():
    return NewsController.get_categories()

@news_bp.route('/api/news/ratings', methods=['GET'])
def get_ratings():
    return NewsController.get_ratings()