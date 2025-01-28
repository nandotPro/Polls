import pytest
from src.validators.auth_validator import AuthValidator
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

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
        with pytest.raises(HttpBadRequestError, match="Body é obrigatório"):
            self.validator.validate_register(request)

    def test_validate_register_missing_field(self):
        # Arrange
        request = HttpRequest(body={"username": "test"})

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Campo email é obrigatório"):
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
        with pytest.raises(HttpUnprocessableEntityError, match="Email inválido"):
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
        with pytest.raises(HttpUnprocessableEntityError, match="Senha deve ter no mínimo 6 caracteres"):
            self.validator.validate_register(request)

    def test_validate_login_success(self):
        # Act & Assert
        self.validator.validate_login(self.valid_login_request)  # Não deve lançar exceção

    def test_validate_login_missing_field(self):
        # Arrange
        request = HttpRequest(body={"email": "test@example.com"})

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Campo password é obrigatório"):
            self.validator.validate_login(request)

    def test_validate_register_invalid_field_types(self):
        # Arrange
        request = HttpRequest(
            body={
                "username": 123,  # deveria ser string
                "email": "test@example.com",
                "password": "test123456"
            }
        )

        # Act & Assert
        with pytest.raises(HttpUnprocessableEntityError, match="Campo username deve ser uma string"):
            self.validator.validate_register(request) 