from src.controllers.poll_controller import PollController
from src.models.mongodb.repository.poll_repository import PollRepository
from src.models.redis.repository.poll_cache_repository import PollCacheRepository
from src.services.jwt_handler import JWTHandler
from src.views.poll_view import PollView
from src.models.mongodb.connection.mongo_connection import mongo_connection_handler
from src.models.redis.connection.redis_connection import redis_connection_handler

class PollComposer:
    @staticmethod
    def compose():
        """Compõe as dependências para enquetes"""
        
        # Connections
        mongo_db = mongo_connection_handler.get_db_connection()
        redis_conn = redis_connection_handler.get_connection()
        
        # Repositories
        poll_repository = PollRepository(mongo_db)
        poll_cache_repository = PollCacheRepository(redis_conn)
        
        # Services
        jwt_handler = JWTHandler()
        
        # Controller
        controller = PollController(
            poll_repository=poll_repository,
            poll_cache_repository=poll_cache_repository,
            auth_handler=jwt_handler
        )
        
        # View
        view = PollView(controller)
        
        return view 