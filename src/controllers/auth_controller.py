from src.models.mongodb.repository.user_repository import UserRepository
from src.models.redis.repository.user_cache_repository import UserCacheRepository
from src.services.jwt_handler import JWTHandler
from src.services.password_handler import PasswordHandler
from src.controllers.interface.auth_controller_interface import AuthControllerInterface
from src.errors.error_types.http_unauthorized import HttpUnauthorizedError
from src.errors.error_types.http_bad_request import HttpBadRequestError

class AuthController(AuthControllerInterface):
    def __init__(
        self,
        user_repository: UserRepository,
        user_cache_repository: UserCacheRepository,
        jwt_handler: JWTHandler,
        password_handler: PasswordHandler
    ):
        self.user_repository = user_repository
        self.user_cache_repository = user_cache_repository
        self.jwt_handler = jwt_handler
        self.password_handler = password_handler

    def register(self, user_data: dict) -> dict:
        """Registra um novo usuário"""
        # Validar dados
        if self.user_repository.find_by_email(user_data["email"]):
            raise HttpBadRequestError("Email já cadastrado")
        
        if self.user_repository.find_by_username(user_data["username"]):
            raise HttpBadRequestError("Username já em uso")

        # Hash da senha
        user_data["password_hash"] = self.password_handler.hash_password(user_data["password"])
        del user_data["password"]

        # Salvar usuário
        user_id = self.user_repository.register_user(user_data)
        
        # Gerar token
        token = self.jwt_handler.generate_token({"user_id": user_id})
        
        return {
            "token": token,
            "user": {
                "id": user_id,
                "username": user_data["username"],
                "email": user_data["email"]
            }
        }

    def login(self, email: str, password: str) -> dict:
        """Realiza login do usuário"""
        # Buscar usuário
        user = self.user_repository.find_by_email(email)
        if not user:
            raise HttpUnauthorizedError("Credenciais inválidas")

        # Verificar senha
        if not self.password_handler.verify_password(password, user["password_hash"]):
            raise HttpUnauthorizedError("Credenciais inválidas")

        # Gerar token
        token = self.jwt_handler.generate_token({"user_id": str(user["_id"])})
        
        # Salvar no cache
        user_data = {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
        self.user_cache_repository.set_user(str(user["_id"]), user_data)

        return {
            "token": token,
            "user": user_data
        } 