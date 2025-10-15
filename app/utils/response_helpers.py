from flask import jsonify
from typing import Any, Dict, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = 200):
    """Respuesta exitosa estandarizada"""
    response = {
        "success": True,
        "message": message,
        "data": data
    }
    return jsonify(response), status_code

def error_response(message: str = "Error", status_code: int = 400, details: Optional[Dict] = None):
    """Respuesta de error estandarizada"""
    response = {
        "success": False,
        "message": message,
        "details": details
    }
    return jsonify(response), status_code

def validation_error_response(errors: Dict):
    """Respuesta para errores de validación"""
    return error_response(
        message="Validation failed",
        status_code=422,
        details={"errors": errors}
    )