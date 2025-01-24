from .interface.view_interface import ViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from src.controllers.interface.auth_controller_interface import AuthControllerInterface
from src.validators.auth_validator import AuthValidator

class AuthView(ViewInterface):
    def __init__(self, controller: AuthControllerInterface):
        self.controller = controller
        self.validator = AuthValidator()

    def _handle_error(self, error: Exception, status_code: int = 400) -> HttpResponse:
        return HttpResponse(
            status_code=status_code,
            body={"error": str(error)}
        )

    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        """Método genérico que será sobrescrito pelos métodos específicos"""
        raise NotImplementedError

    async def register(self, http_request: HttpRequest) -> HttpResponse:
        """Processa requisição de registro"""
        try:
            self.validator.validate_register(http_request)
            
            result = await self.controller.register(http_request.body)
            
            return HttpResponse(
                status_code=201,
                body=result
            )
            
        except ValueError as error:
            return self._handle_error(error)
            
        except Exception as error:
            return self._handle_error(error, 500)

    async def login(self, http_request: HttpRequest) -> HttpResponse:
        """Processa requisição de login"""
        try:
            self.validator.validate_login(http_request)
            
            result = await self.controller.login(
                http_request.body["email"],
                http_request.body["password"]
            )
            
            return HttpResponse(
                status_code=200,
                body=result
            )
            
        except ValueError as error:
            return self._handle_error(error, 401)
            
        except Exception as error:
            return self._handle_error(error, 500) 