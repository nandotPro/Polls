import pytest
from src.validators.auth_validator import AuthValidator
from src.views.http_types.http_request import HttpRequest

class TestAuthValidator:
    def setup_method(self):
        self.validator = AuthValidator()
        self.valid_register_request = HttpRequest(
            body={
                "username": "testuser",
                "email": "test@example.com",
                "password": "test123456"
            }
        )
        self.valid_login_request = HttpRequest(
            body={
                "email": "test@example.com",
                "password": "test123456"
            }
        )

    def test_validate_register_success(self):
        # Act & Assert
        self.validator.validate_register(self.valid_register_request)  # Não deve lançar exceção

    def test_validate_register_missing_body(self):
        # Arrange
        request = HttpRequest()

        # Act & Assert
        with pytest.raises(ValueError, match="Body é obrigatório"):
            self.validator.validate_register(request)

    def test_validate_register_missing_field(self):
        # Arrange
        request = HttpRequest(body={"username": "test"})

        # Act & Assert
        with pytest.raises(ValueError, match="Campo email é obrigatório"):
            self.validator.validate_register(request)

    def test_validate_register_invalid_email(self):
        # Arrange
        request = HttpRequest(
            body={
                "username": "testuser",
                "email": "invalid-email",
                "password": "test123456"
            }
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Email inválido"):
            self.validator.validate_register(request)

    def test_validate_register_short_password(self):
        # Arrange
        request = HttpRequest(
            body={
                "username": "testuser",
                "email": "test@example.com",
                "password": "123"
            }
        )

        # Act & Assert
        with pytest.raises(ValueError, match="Senha deve ter no mínimo 6 caracteres"):
            self.validator.validate_register(request)

    def test_validate_login_success(self):
        # Act & Assert
        self.validator.validate_login(self.valid_login_request)  # Não deve lançar exceção

    def test_validate_login_missing_field(self):
        # Arrange
        request = HttpRequest(body={"email": "test@example.com"})

        # Act & Assert
        with pytest.raises(ValueError, match="Campo password é obrigatório"):
            self.validator.validate_login(request) 