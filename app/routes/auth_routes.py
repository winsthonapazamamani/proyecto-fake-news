from flask import Blueprint
from ..controllers.auth_controller import AuthController  # Import relativo

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    return AuthController.register()

@auth_bp.route('/login', methods=['POST'])
def login():
    return AuthController.login()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return AuthController.logout()