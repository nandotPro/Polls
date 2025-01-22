import pytest
from datetime import datetime, timedelta
from src.services.jwt_handler import JWTHandler
import jwt
import os
from dotenv import load_dotenv

class TestJWTHandler:
    @classmethod
    def setup_class(cls):
        """Configuração que roda uma vez antes de todos os testes"""
        # Guarda o valor original se existir
        cls.original_secret = os.getenv("JWT_SECRET")
        # Define um valor específico para testes
        os.environ["JWT_SECRET"] = "test_secret_key"

    def setup_method(self):
        """Configuração que roda antes de cada teste"""
        self.jwt_handler = JWTHandler()
        self.test_payload = {"user_id": "123"}

    def test_generate_token_success(self):
        # Arrange & Act
        token = self.jwt_handler.generate_token(self.test_payload.copy())
        
        # Assert
        assert token is not None
        decoded = jwt.decode(
            token, 
            os.environ["JWT_SECRET"], 
            algorithms=["HS256"]
        )
        assert decoded["user_id"] == self.test_payload["user_id"]
        assert isinstance(decoded["exp"], int)
        assert decoded["exp"] > int(datetime.now().timestamp())

    def test_validate_token_success(self):
        # Arrange
        token = self.jwt_handler.generate_token(self.test_payload.copy())
        
        # Act
        payload = self.jwt_handler.validate_token(token)
        
        # Assert
        assert payload["user_id"] == self.test_payload["user_id"]
        assert isinstance(payload["exp"], int)

    def test_validate_expired_token(self):
        # Arrange
        expired_payload = {
            "user_id": "123",
            "exp": int(datetime.now().timestamp()) - 86400  # 24 horas atrás
        }
        token = jwt.encode(
            expired_payload, 
            os.environ["JWT_SECRET"], 
            algorithm="HS256"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Token expirado"):
            self.jwt_handler.validate_token(token)

    def test_validate_invalid_token(self):
        # Arrange
        invalid_token = "invalid.token.here"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Token inválido"):
            self.jwt_handler.validate_token(invalid_token)

    @classmethod
    def teardown_class(cls):
        """Limpeza que roda uma vez depois de todos os testes"""
        if cls.original_secret:
            # Restaura o valor original se existia
            os.environ["JWT_SECRET"] = cls.original_secret
        else:
            # Remove se não existia
            del os.environ["JWT_SECRET"] 