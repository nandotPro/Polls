from flask import Blueprint, request, jsonify
from src.main.composers.auth_composer import AuthComposer
from src.views.http_types.http_request import HttpRequest

auth_routes_bp = Blueprint('auth_routes', __name__)
auth_view = AuthComposer.compose()

@auth_routes_bp.route('/register', methods=['POST'])
async def register():
    try:
        http_request = HttpRequest(
            body=request.json
        )
        response = await auth_view.register(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@auth_routes_bp.route('/login', methods=['POST'])
async def login():
    try:
        http_request = HttpRequest(
            body=request.json
        )
        response = await auth_view.login(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500 