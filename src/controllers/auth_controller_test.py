import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.controllers.auth_controller import AuthController
from src.models.mongodb.repository.user_repository import UserRepository
from src.models.redis.repository.user_cache_repository import UserCacheRepository

class TestAuthController:
    def setup_method(self):
        # Criar mocks para os repositórios
        self.user_repository_mock = Mock(spec=UserRepository)
        self.user_cache_repository_mock = Mock(spec=UserCacheRepository)
        
        # Configurar métodos assíncronos
        self.user_repository_mock.find_by_email = AsyncMock()
        self.user_repository_mock.find_by_username = AsyncMock()
        self.user_repository_mock.register_user = AsyncMock()
        self.user_cache_repository_mock.set_user = AsyncMock()

        # Criar controller com os mocks
        with patch('src.controllers.auth_controller.UserRepository', return_value=self.user_repository_mock), \
             patch('src.controllers.auth_controller.UserCacheRepository', return_value=self.user_cache_repository_mock):
            self.auth_controller = AuthController()

        # Dados de teste
        self.test_user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123"
        }

    @pytest.mark.asyncio
    async def test_register_success(self):
        # Arrange
        self.user_repository_mock.find_by_email.return_value = None
        self.user_repository_mock.find_by_username.return_value = None
        self.user_repository_mock.register_user.return_value = "user123"
        self.auth_controller.jwt_handler.generate_token = Mock(return_value="test.token.here")

        # Act
        result = await self.auth_controller.register(self.test_user_data.copy())

        # Assert
        assert result["token"] == "test.token.here"
        assert result["user"]["username"] == self.test_user_data["username"]
        assert "password" not in result["user"]
        self.user_repository_mock.register_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self):
        # Arrange
        self.user_repository_mock.find_by_email.return_value = {"email": self.test_user_data["email"]}

        # Act & Assert
        with pytest.raises(ValueError, match="Email já cadastrado"):
            await self.auth_controller.register(self.test_user_data.copy())

    @pytest.mark.asyncio
    async def test_login_success(self):
        # Arrange
        test_user = {
            "_id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password"
        }
        self.user_repository_mock.find_by_email.return_value = test_user
        self.auth_controller.password_handler.verify_password = Mock(return_value=True)
        self.auth_controller.jwt_handler.generate_token = Mock(return_value="test.token.here")

        # Act
        result = await self.auth_controller.login("test@example.com", "test123")

        # Assert
        assert result["token"] == "test.token.here"
        assert result["user"]["email"] == test_user["email"]
        assert "password_hash" not in result["user"]
        self.user_cache_repository_mock.set_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self):
        # Arrange
        self.user_repository_mock.find_by_email.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Credenciais inválidas"):
            await self.auth_controller.login("wrong@email.com", "wrong_password") 