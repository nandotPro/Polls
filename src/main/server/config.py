from flask import Flask
from flask_cors import CORS
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler
from src.models.redis.connection.redis_connection import redis_connection_handler
from src.errors.error_handler import handle_errors
from src.errors.error_types.http_error import HttpError

def create_app():
    app = Flask(__name__)
    
    # Configurações
    CORS(app)
    app.config['JSON_SORT_KEYS'] = False
    
    # Inicializar conexões primeiro
    mongo_connection_handler.connect_to_db()
    redis_connection_handler.connect()
    
    # Importar rotas depois das conexões
    from src.main.routes.auth_routes import auth_routes_bp
    from src.main.routes.poll_routes import poll_routes_bp
    
    # Registrar blueprints
    app.register_blueprint(auth_routes_bp, url_prefix='/auth')
    app.register_blueprint(poll_routes_bp, url_prefix='/polls')
    
    # Registrar handler de erros
    app.register_error_handler(HttpError, handle_errors)
    app.register_error_handler(Exception, handle_errors)
    
    return app 