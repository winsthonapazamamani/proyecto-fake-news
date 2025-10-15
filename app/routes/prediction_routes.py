from flask import Blueprint
from app.controllers.prediction_controller import PredictionController

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/api/predict/classify', methods=['POST'])
def classify_news():
    return PredictionController.classify_news()

@prediction_bp.route('/api/predict/history', methods=['GET'])
def get_prediction_history():
    return PredictionController.get_prediction_history()

@prediction_bp.route('/api/predict/history/<int:prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    return PredictionController.get_prediction(prediction_id)

@prediction_bp.route('/api/predict/stats', methods=['GET'])
def get_prediction_stats():
    return PredictionController.get_prediction_stats()