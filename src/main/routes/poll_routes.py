from flask import Blueprint, request, jsonify
from src.main.composers.poll_composer import PollComposer
from src.views.http_types.http_request import HttpRequest

poll_routes_bp = Blueprint('poll_routes', __name__)
poll_view = PollComposer.compose()

@poll_routes_bp.route('/', methods=['POST'])
async def create_poll():
    try:
        http_request = HttpRequest(
            headers={"Authorization": request.headers.get("Authorization")},
            body=request.json
        )
        response = await poll_view.create_poll(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@poll_routes_bp.route('/<poll_id>/vote', methods=['POST'])
async def vote():
    try:
        http_request = HttpRequest(
            headers={"Authorization": request.headers.get("Authorization")},
            body=request.json
        )
        response = await poll_view.vote(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@poll_routes_bp.route('/<poll_id>', methods=['GET'])
async def get_poll(poll_id):
    try:
        http_request = HttpRequest(
            query_params={"poll_id": poll_id}
        )
        response = await poll_view.get_poll(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@poll_routes_bp.route('/', methods=['GET'])
async def list_polls():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        http_request = HttpRequest(
            query_params={
                "page": page,
                "limit": limit
            }
        )
        response = await poll_view.list_polls(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500

@poll_routes_bp.route('/user', methods=['GET'])
async def get_user_polls():
    try:
        http_request = HttpRequest(
            headers={"Authorization": request.headers.get("Authorization")}
        )
        response = await poll_view.get_user_polls(http_request)
        
        return jsonify(response.body), response.status_code
    
    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500 