from flask import jsonify
from .error_types.http_unprocessable_entity import HttpUnprocessableEntityError
from .error_types.http_bad_request import HttpBadRequestError
from .error_types.http_unauthorized import HttpUnauthorizedError
from .error_types.http_not_found import HttpNotFoundError

def handle_errors(error):
    """Trata os erros da aplicação"""
    
    if isinstance(error, HttpUnprocessableEntityError):
        return jsonify({
            "error": {
                "status": error.status_code,
                "title": error.name,
                "detail": error.message
            }
        }), error.status_code

    if isinstance(error, HttpBadRequestError):
        return jsonify({
            "error": {
                "status": error.status_code,
                "title": error.name,
                "detail": error.message
            }
        }), error.status_code

    if isinstance(error, HttpUnauthorizedError):
        return jsonify({
            "error": {
                "status": error.status_code,
                "title": error.name,
                "detail": error.message
            }
        }), error.status_code

    if isinstance(error, HttpNotFoundError):
        return jsonify({
            "error": {
                "status": error.status_code,
                "title": error.name,
                "detail": error.message
            }
        }), error.status_code

    # Erro genérico
    return jsonify({
        "error": {
            "status": 500,
            "title": "Internal Server Error",
            "detail": str(error)
        }
    }), 500 