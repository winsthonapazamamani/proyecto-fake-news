from flask import request
from models.prediction import Prediction
from config.database import db
from utils.response_helpers import success_response, error_response
from utils.text_preprocessor import clean_text
import os

class PredictionController:
    @staticmethod
    def predict():
        try:
            data = request.get_json()
            text = data.get('text', '').strip()
            
            if not text:
                return error_response("Text is required", 400)
            
            # Aquí iría la lógica de predicción con el modelo ML
            # Por ahora, mock response
            processed_text = clean_text(text)
            
            # Simulación de predicción
            prediction_result = 1 if len(processed_text) > 50 else 0
            confidence = 0.85
            
            # Guardar en base de datos
            new_prediction = Prediction(
                news_text=text,
                prediction_result=prediction_result,
                confidence=confidence,
                probabilities={"class_0": 0.15, "class_1": 0.85}
            )
            
            db.session.add(new_prediction)
            db.session.commit()
            
            return success_response(
                data={
                    'prediction': prediction_result,
                    'confidence': confidence,
                    'probabilities': {"class_0": 0.15, "class_1": 0.85},
                    'processed_text': processed_text,
                    'prediction_id': new_prediction.id
                },
                message="Prediction completed successfully"
            )
            
        except Exception as e:
            db.session.rollback()
            return error_response(f"Prediction failed: {str(e)}", 500)
    
    @staticmethod
    def get_predictions():
        """Obtiene historial de predicciones"""
        try:
            predictions = Prediction.query.order_by(Prediction.created_at.desc()).limit(50).all()
            return success_response(
                data=[pred.to_dict() for pred in predictions],
                message="Predictions retrieved successfully"
            )
        except Exception as e:
            return error_response(f"Failed to get predictions: {str(e)}", 500)