from flask import request
import secrets
from app.controllers.base_controller import BaseController
from app.models.user import User

class AuthController(BaseController):
    """Controller for authentication operations"""
    
    # Simple token storage (in production use Redis or database)
    _tokens = {}
    
    @classmethod
    def register(cls):
        """Register a new user"""
        try:
            data = request.get_json()
            
            # Validate required fields
            is_valid, error_message = cls.validate_required_fields(
                data, ['username', 'email', 'password']
            )
            if not is_valid:
                return cls.error_response(error_message, 400)
            
            # Validate email format
            if not cls._validate_email(data['email']):
                return cls.error_response("Invalid email format", 400)
            
            # Validate password strength
            is_password_valid, password_error = cls._validate_password(data['password'])
            if not is_password_valid:
                return cls.error_response(password_error, 400)
            
            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return cls.error_response("Username already exists", 400)
                
            if User.query.filter_by(email=data['email']).first():
                return cls.error_response("Email already exists", 400)
            
            def register_operation():
                user = User(
                    username=data['username'].strip(),
                    email=data['email'].strip().lower()
                )
                user.set_password(data['password'])
                db.session.add(user)
                return user
            
            success, result, message = cls.handle_database_operation(
                register_operation,
                "User registered successfully"
            )
            
            if success:
                # Generate token
                token = cls._generate_token(result.id)
                
                return cls.success_response(
                    data={
                        'user': result.to_dict(),
                        'token': token
                    },
                    message=message,
                    status_code=201
                )
            else:
                return cls.error_response(message, 500)
                
        except Exception as e:
            return cls.error_response(f"Error during registration: {str(e)}", 500)
    
    @classmethod
    def login(cls):
        """Login user and return token"""
        try:
            data = request.get_json()
            
            # Validate required fields
            is_valid, error_message = cls.validate_required_fields(
                data, ['username', 'password']
            )
            if not is_valid:
                return cls.error_response(error_message, 400)
            
            # Find user
            user = User.query.filter_by(username=data['username']).first()
            
            if not user or not user.check_password(data['password']):
                return cls.error_response("Invalid username or password", 401)
            
            if not user.is_active:
                return cls.error_response("Account is deactivated", 403)
            
            # Generate token
            token = cls._generate_token(user.id)
            
            return cls.success_response(
                data={
                    'user': user.to_dict(),
                    'token': token
                },
                message="Login successful"
            )
            
        except Exception as e:
            return cls.error_response(f"Error during login: {str(e)}", 500)
    
    @classmethod
    def get_profile(cls):
        """Get current user profile"""
        try:
            user = cls._get_current_user()
            if not user:
                return cls.error_response("Invalid or missing token", 401)
            
            return cls.success_response(
                data=user.to_dict(),
                message="Profile retrieved successfully"
            )
            
        except Exception as e:
            return cls.error_response(f"Error retrieving profile: {str(e)}", 500)
    
    @classmethod
    def _get_current_user(cls):
        """Get user from token"""
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = cls._tokens.get(token)
        if user_id:
            return User.query.get(user_id)
        return None
    
    @classmethod
    def _generate_token(cls, user_id):
        """Generate a new authentication token"""
        token = secrets.token_hex(32)
        cls._tokens[token] = user_id
        return token
    
    @classmethod
    def _validate_email(cls, email):
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @classmethod
    def _validate_password(cls, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        
        return True, "Password is valid"
    
    @classmethod
    def logout(cls):
        """Logout user by invalidating token"""
        try:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if token in cls._tokens:
                del cls._tokens[token]
            
            return cls.success_response(
                message="Logout successful"
            )
            
        except Exception as e:
            return cls.error_response(f"Error during logout: {str(e)}", 500)
        