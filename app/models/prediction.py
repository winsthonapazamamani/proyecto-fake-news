from config.database import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    news_text = db.Column(db.Text, nullable=False)
    prediction_result = db.Column(db.Integer, nullable=False)  # 0: Negative, 1: Positive
    confidence = db.Column(db.Float, nullable=False)
    probabilities = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'news_text_preview': self.news_text[:100] + '...' if len(self.news_text) > 100 else self.news_text,
            'prediction_result': self.prediction_result,
            'confidence': self.confidence,
            'probabilities': self.probabilities,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }