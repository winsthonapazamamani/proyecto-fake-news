import hashlib
import secrets
from datetime import datetime, timedelta
import jwt
import os

def generate_token(user_id, expires_in=3600):
    """Genera un token JWT"""
    secret_key = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token):
    """Verifica un token JWT"""
    try:
        secret_key = os.getenv('JWT_SECRET_KEY', 'fallback-secret-key')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def hash_password(password):
    """Hash de contraseña simple (mejorar con bcrypt en producción)"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_api_key():
    """Genera una API key única"""
    return secrets.token_urlsafe(32)