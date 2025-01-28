from .interface.view_interface import ViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from src.controllers.interface.auth_controller_interface import AuthControllerInterface
from src.validators.auth_validator import AuthValidator
from src.errors.error_types.http_unauthorized import HttpUnauthorizedError
from src.errors.error_types.http_bad_request import HttpBadRequestError

class AuthView(ViewInterface):
    def __init__(self, controller: AuthControllerInterface):
        self.controller = controller
        self.validator = AuthValidator()

    def _handle_error(self, error: Exception, status_code: int = 400) -> HttpResponse:
        raise error

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Método genérico que será sobrescrito pelos métodos específicos"""
        raise NotImplementedError

    def register(self, http_request: HttpRequest) -> HttpResponse:
        """Processa requisição de registro"""
        try:
            self.validator.validate_register(http_request)
            result = self.controller.register(http_request.body)
            return HttpResponse(status_code=201, body=result)
        except Exception as error:
            raise error

    def login(self, http_request: HttpRequest) -> HttpResponse:
        """Processa requisição de login"""
        try:
            self.validator.validate_login(http_request)
            result = self.controller.login(
                http_request.body["email"],
                http_request.body["password"]
            )
            return HttpResponse(status_code=200, body=result)
        except Exception as error:
            raise error 