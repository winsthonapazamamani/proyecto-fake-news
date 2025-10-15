import re
import datetime
from urllib.parse import urlparse

class Validators:
    """Utility class for data validation operations"""
    
    # Email validation regex
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    # URL validation regex
    URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    @classmethod
    def validate_email(cls, email):
        """
        Validate email format
        """
        if not email or not isinstance(email, str):
            return False, "Email must be a non-empty string"
        
        if not cls.EMAIL_REGEX.match(email):
            return False, "Invalid email format"
        
        return True, "Email is valid"
    
    @classmethod
    def validate_password(cls, password):
        """
        Validate password strength
        """
        if not password or not isinstance(password, str):
            return False, "Password must be a non-empty string"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        
        if not any(char.islower() for char in password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for common weak passwords
        weak_passwords = ['password', '12345678', 'qwerty', 'admin', 'letmein']
        if password.lower() in weak_passwords:
            return False, "Password is too common, choose a stronger one"
        
        return True, "Password is valid"
    
    @classmethod
    def validate_url(cls, url):
        """
        Validate URL format
        """
        if not url:
            return True, "URL is optional"  # URLs can be optional
        
        if not isinstance(url, str):
            return False, "URL must be a string"
        
        if not cls.URL_REGEX.match(url):
            return False, "Invalid URL format"
        
        return True, "URL is valid"
    
    @classmethod
    def validate_date(cls, date_string, date_format='%Y-%m-%d'):
        """
        Validate date string format
        """
        if not date_string:
            return True, "Date is optional"
        
        try:
            datetime.datetime.strptime(date_string, date_format)
            return True, "Date is valid"
        except ValueError:
            return False, f"Date must be in format {date_format}"
    
    @classmethod
    def validate_news_article(cls, data):
        """
        Validate news article data
        """
        errors = []
        
        # Validate title
        if not data.get('title') or not isinstance(data['title'], str):
            errors.append("Title is required and must be a string")
        elif len(data['title'].strip()) < 5:
            errors.append("Title must be at least 5 characters long")
        elif len(data['title'].strip()) > 500:
            errors.append("Title must be less than 500 characters")
        
        # Validate content
        if not data.get('content') or not isinstance(data['content'], str):
            errors.append("Content is required and must be a string")
        elif len(data['content'].strip()) < 10:
            errors.append("Content must be at least 10 characters long")
        elif len(data['content'].strip()) > 10000:
            errors.append("Content must be less than 10,000 characters")
        
        # Validate source (optional)
        if data.get('source') and len(data['source']) > 500:
            errors.append("Source must be less than 500 characters")
        
        # Validate URL (optional)
        if data.get('url'):
            is_valid, url_error = cls.validate_url(data['url'])
            if not is_valid:
                errors.append(url_error)
        
        # Validate category (optional)
        valid_categories = [
            'POLITICA', 'SALUD', 'ECONOMIA', 'EDUCACION', 'SEGURIDAD',
            'CORRUPCION', 'REDES_SOCIALES', 'INTERNACIONAL', 'GOBIERNO',
            'CONGRESO', 'ELECCIONES', 'COVID19', 'VACUNAS', 'OTROS'
        ]
        if data.get('category') and data['category'] not in valid_categories:
            errors.append(f"Category must be one of: {', '.join(valid_categories)}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def validate_user_registration(cls, data):
        """
        Validate user registration data
        """
        errors = []
        
        # Validate username
        if not data.get('username') or not isinstance(data['username'], str):
            errors.append("Username is required and must be a string")
        elif len(data['username'].strip()) < 3:
            errors.append("Username must be at least 3 characters long")
        elif len(data['username'].strip()) > 50:
            errors.append("Username must be less than 50 characters")
        elif not re.match(r'^[a-zA-Z0-9_]+$', data['username']):
            errors.append("Username can only contain letters, numbers, and underscores")
        
        # Validate email
        if not data.get('email'):
            errors.append("Email is required")
        else:
            is_valid, email_error = cls.validate_email(data['email'])
            if not is_valid:
                errors.append(email_error)
        
        # Validate password
        if not data.get('password'):
            errors.append("Password is required")
        else:
            is_valid, password_error = cls.validate_password(data['password'])
            if not is_valid:
                errors.append(password_error)
        
        return len(errors) == 0, errors
    
    @classmethod
    def sanitize_input(cls, input_string, max_length=None):
        """
        Sanitize input string by removing potentially dangerous characters
        """
        if not input_string:
            return ""
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', str(input_string))
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        # Apply length limit if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @classmethod
    def is_valid_category(cls, category):
        """
        Check if category is valid
        """
        valid_categories = [
            'POLITICA', 'SALUD', 'ECONOMIA', 'EDUCACION', 'SEGURIDAD',
            'CORRUPCION', 'REDES_SOCIALES', 'INTERNACIONAL', 'GOBIERNO',
            'CONGRESO', 'ELECCIONES', 'COVID19', 'VACUNAS', 'OTROS'
        ]
        return category in valid_categories
    
    @classmethod
    def is_valid_rating(cls, rating):
        """
        Check if rating is valid
        """
        valid_ratings = [
            'FALSO', 'VERDADERO', 'ENGAÑOSO', 'EXAGERADO',
            'SIN_EVIDENCIAS', 'CONTEXTO_ERRONEO', 'DESACTUALIZADO'
        ]
        return rating in valid_ratings

# Example usage
if __name__ == "__main__":
    # Test validators
    print("Email validation:", Validators.validate_email("test@example.com"))
    print("Password validation:", Validators.validate_password("StrongPass123"))
    print("URL validation:", Validators.validate_url("https://example.com"))
    print("Date validation:", Validators.validate_date("2023-12-25"))
    
    test_article = {
        "title": "Test Article",
        "content": "This is a test content for validation.",
        "source": "Test Source",
        "url": "https://example.com",
        "category": "POLITICA"
    }
    print("Article validation:", Validators.validate_news_article(test_article))