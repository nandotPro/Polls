from src.controllers.auth_controller import AuthController
from src.models.mongodb.repository.user_repository import UserRepository
from src.models.redis.repository.user_cache_repository import UserCacheRepository
from src.services.jwt_handler import JWTHandler
from src.services.password_handler import PasswordHandler
from src.views.auth_view import AuthView
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler
from src.models.redis.connection.redis_connection import redis_connection_handler

class AuthComposer:
    @staticmethod
    def compose():
        """Compõe as dependências para autenticação"""
        
        # Connections
        mongo_db = mongo_connection_handler.get_db_connection()
        redis_conn = redis_connection_handler.get_connection()
        
        # Repositories
        user_repository = UserRepository(mongo_db)
        user_cache_repository = UserCacheRepository(redis_conn)
        
        # Services
        jwt_handler = JWTHandler()
        password_handler = PasswordHandler()
        
        # Controller
        controller = AuthController(
            user_repository=user_repository,
            user_cache_repository=user_cache_repository,
            jwt_handler=jwt_handler,
            password_handler=password_handler
        )
        
        # View
        view = AuthView(controller)
        
        return view 