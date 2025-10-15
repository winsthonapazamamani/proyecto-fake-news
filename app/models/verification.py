from app import db
from datetime import datetime
import json

class Verification(db.Model):
    """Model for Amallulla verifications"""
    __tablename__ = 'verificaciones_amallulla'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo_afirmacion = db.Column(db.Text, nullable=False)
    contenido_afirmacion = db.Column(db.Text, nullable=False)
    contexto_afirmacion = db.Column(db.Text)
    fuente_original = db.Column(db.String(500))
    medio_difusion = db.Column(db.String(255))
    fecha_afirmacion = db.Column(db.Date)
    fecha_verificacion = db.Column(db.Date)
    categoria_afirmacion = db.Column(db.String(100))
    calificacion_amallulla = db.Column(db.String(50))
    explicacion_verificacion = db.Column(db.Text)
    viralizacion_redes = db.Column(db.Boolean, default=False)
    impacto_calificacion = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'titulo_afirmacion': self.titulo_afirmacion,
            'contenido_afirmacion': self.contenido_afirmacion,
            'categoria_afirmacion': self.categoria_afirmacion,
            'calificacion_amallulla': self.calificacion_amallulla,
            'fuente_original': self.fuente_original,
            'explicacion_verificacion': self.explicacion_verificacion,
            'viralizacion_redes': self.viralizacion_redes,
            'impacto_calificacion': self.impacto_calificacion,
            'fecha_verificacion': self.fecha_verificacion.isoformat() if self.fecha_verificacion else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }