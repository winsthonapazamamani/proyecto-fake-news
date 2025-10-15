from flask import jsonify
from utils.response_helpers import success_response, error_response

class BaseController:
    @staticmethod
    def handle_success(data=None, message="Success", status_code=200):
        return success_response(data, message, status_code)
    
    @staticmethod
    def handle_error(message="Error", status_code=400, details=None):
        return error_response(message, status_code, details)