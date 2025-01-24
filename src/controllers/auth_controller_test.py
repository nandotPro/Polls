import pytest
from unittest.mock import Mock, AsyncMock
from src.controllers.auth_controller import AuthController

class TestAuthController:
    def setup_method(self):
        # Criar mocks
        self.user_repository = Mock()
        self.user_cache_repository = Mock()
        self.jwt_handler = Mock()
        self.password_handler = Mock()

        # Configurar métodos assíncronos
        self.user_repository.find_by_email = AsyncMock()
        self.user_repository.find_by_username = AsyncMock()
        self.user_repository.register_user = AsyncMock()
        self.user_cache_repository.set_user = AsyncMock()

        # Configurar controller com mocks
        self.auth_controller = AuthController(
            user_repository=self.user_repository,
            user_cache_repository=self.user_cache_repository,
            jwt_handler=self.jwt_handler,
            password_handler=self.password_handler
        )

        # Dados de teste
        self.user_data = {
            "username": "test_user",
            "email": "test@mail.com",
            "password": "test123"
        }

    @pytest.mark.asyncio
    async def test_register_success(self):
        # Arrange
        self.user_repository.find_by_email.return_value = None
        self.user_repository.find_by_username.return_value = None
        self.user_repository.register_user.return_value = "fake_id"
        self.password_handler.hash_password.return_value = "hashed_password"
        self.jwt_handler.generate_token.return_value = "fake_token"

        # Act
        result = await self.auth_controller.register(self.user_data)

        # Assert
        assert result["token"] == "fake_token"
        assert result["user"]["id"] == "fake_id"
        assert result["user"]["username"] == self.user_data["username"]
        self.user_repository.register_user.assert_called_once()

    @pytest.mark.asyncio
    async def test_register_email_exists(self):
        # Arrange
        self.user_repository.find_by_email.return_value = {"email": self.user_data["email"]}

        # Act & Assert
        with pytest.raises(ValueError, match="Email já cadastrado"):
            await self.auth_controller.register(self.user_data)

    @pytest.mark.asyncio
    async def test_login_success(self):
        # Arrange
        fake_user = {
            "_id": "fake_id",
            "username": "test_user",
            "email": "test@mail.com",
            "password_hash": "hashed_password"
        }
        self.user_repository.find_by_email.return_value = fake_user
        self.password_handler.verify_password.return_value = True
        self.jwt_handler.generate_token.return_value = "fake_token"

        # Act
        result = await self.auth_controller.login(
            self.user_data["email"],
            self.user_data["password"]
        )

        # Assert
        assert result["token"] == "fake_token"
        assert result["user"]["id"] == "fake_id"
        self.user_cache_repository.set_user.assert_called_once() 