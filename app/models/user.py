from config.database import db
from datetime import datetime
from utils.security_utils import hash_password

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    
    def set_password(self, password):
        """Establece la contraseña hasheada"""
        self.password_hash = hash_password(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return self.password_hash == hash_password(password)
    
    def to_dict(self):
        """Convierte el modelo a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }