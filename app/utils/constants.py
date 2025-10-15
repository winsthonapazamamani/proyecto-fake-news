class Constants:
    """Application constants"""
    
    # API Configuration
    API_VERSION = "1.0.0"
    MAX_PAGE_SIZE = 100
    DEFAULT_PAGE_SIZE = 10
    
    # News Categories
    CATEGORIES = [
        'POLITICA',
        'SALUD', 
        'ECONOMIA',
        'EDUCACION',
        'SEGURIDAD',
        'CORRUPCION',
        'REDES_SOCIALES',
        'INTERNACIONAL',
        'GOBIERNO',
        'CONGRESO',
        'ELECCIONES',
        'COVID19',
        'VACUNAS',
        'OTROS'
    ]
    
    # Verification Ratings
    RATINGS = [
        'FALSO',
        'VERDADERO',
        'ENGAÑOSO', 
        'EXAGERADO',
        'SIN_EVIDENCIAS',
        'CONTEXTO_ERRONEO',
        'DESACTUALIZADO'
    ]
    
    # Impact Levels
    IMPACT_LEVELS = ['ALTO', 'MEDIO', 'BAJO']
    
    # Political Figure Roles
    POLITICAL_ROLES = [
        'SUJETO',
        'FUENTE',
        'AFIRMANTE',
        'BENEFICIADO', 
        'AFECTADO',
        'MENCIÓN'
    ]
    
    # Social Media Platforms
    PLATFORMS = [
        'Facebook',
        'Twitter',
        'WhatsApp', 
        'TikTok',
        'Instagram',
        'YouTube'
    ]
    
    # ML Model Configuration
    ML_CONFIG = {
        'MAX_TEXT_LENGTH': 1000,
        'MIN_TEXT_LENGTH': 10,
        'DEFAULT_CONFIDENCE_THRESHOLD': 0.7,
        'MODEL_VERSIONS': ['mock-v1.0', 'lstm-v1.0', 'bert-v1.0']
    }
    
    # Error Messages
    ERROR_MESSAGES = {
        'VALIDATION_ERROR': 'Validation failed',
        'NOT_FOUND': 'Resource not found',
        'UNAUTHORIZED': 'Unauthorized access',
        'FORBIDDEN': 'Access forbidden',
        'DATABASE_ERROR': 'Database operation failed',
        'NETWORK_ERROR': 'Network connection failed',
        'RATE_LIMIT_EXCEEDED': 'Rate limit exceeded',
        'INVALID_TOKEN': 'Invalid or expired token'
    }
    
    # Success Messages
    SUCCESS_MESSAGES = {
        'CREATED': 'Resource created successfully',
        'UPDATED': 'Resource updated successfully',
        'DELETED': 'Resource deleted successfully',
        'RETRIEVED': 'Resource retrieved successfully',
        'OPERATION_COMPLETED': 'Operation completed successfully'
    }
    
    # HTTP Status Codes
    HTTP_STATUS = {
        'OK': 200,
        'CREATED': 201,
        'NO_CONTENT': 204,
        'BAD_REQUEST': 400,
        'UNAUTHORIZED': 401,
        'FORBIDDEN': 403,
        'NOT_FOUND': 404,
        'INTERNAL_ERROR': 500,
        'SERVICE_UNAVAILABLE': 503
    }
    
    # Database Configuration
    DB_CONFIG = {
        'MAX_CONNECTIONS': 20,
        'POOL_RECYCLE': 3600,
        'CONNECTION_TIMEOUT': 30
    }
    
    # Security Configuration
    SECURITY_CONFIG = {
        'PASSWORD_MIN_LENGTH': 8,
        'TOKEN_EXPIRY_HOURS': 24,
        'MAX_LOGIN_ATTEMPTS': 5,
        'LOCKOUT_DURATION_MINUTES': 30
    }

# Example usage
if __name__ == "__main__":
    print("Available categories:", Constants.CATEGORIES)
    print("Available ratings:", Constants.RATINGS)
    print("API Version:", Constants.API_VERSION)