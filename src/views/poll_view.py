from .interface.view_interface import ViewInterface
from .http_types.http_request import HttpRequest
from .http_types.http_response import HttpResponse
from src.controllers.interface.poll_controller_interface import PollControllerInterface
from src.validators.poll_validator import PollValidator

class PollView(ViewInterface):
    def __init__(self, controller: PollControllerInterface):
        self.controller = controller
        self.validator = PollValidator()

    def _handle_error(self, error: Exception, status_code: int = 400) -> HttpResponse:
        return HttpResponse(
            status_code=status_code,
            body={"error": str(error)}
        )

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    def create_poll(self, http_request: HttpRequest) -> HttpResponse:
        try:
            self.validator.validate_create_poll(http_request)
            token = http_request.headers.get("Authorization")
            
            result = self.controller.create_poll(http_request.body, token)
            return HttpResponse(status_code=201, body=result)
            
        except ValueError as error:
            return self._handle_error(error)
        except Exception as error:
            return self._handle_error(error, 500)

    def vote(self, http_request: HttpRequest) -> HttpResponse:
        try:
            self.validator.validate_vote(http_request)
            token = http_request.headers.get("Authorization")
            
            result = self.controller.vote(
                http_request.body["poll_id"],
                http_request.body["option_index"],
                token
            )
            return HttpResponse(status_code=200, body=result)
            
        except ValueError as error:
            return self._handle_error(error)
        except Exception as error:
            return self._handle_error(error, 500)

    def get_poll(self, http_request: HttpRequest) -> HttpResponse:
        try:
            poll_id = http_request.query_params.get("poll_id")
            if not poll_id:
                raise ValueError("poll_id é obrigatório")
                
            result = self.controller.get_poll(poll_id)
            return HttpResponse(status_code=200, body=result)
            
        except ValueError as error:
            return self._handle_error(error)
        except Exception as error:
            return self._handle_error(error, 500)

    def list_polls(self, http_request: HttpRequest) -> HttpResponse:
        try:
            page = int(http_request.query_params.get("page", 1))
            limit = int(http_request.query_params.get("limit", 10))
            
            result = self.controller.list_polls(page, limit)
            return HttpResponse(status_code=200, body=result)
            
        except ValueError as error:
            return self._handle_error(error)
        except Exception as error:
            return self._handle_error(error, 500)

    def get_user_polls(self, http_request: HttpRequest) -> HttpResponse:
        try:
            token = http_request.headers.get("Authorization")
            if not token:
                raise ValueError("Token é obrigatório")
                
            result = self.controller.get_user_polls(token)
            return HttpResponse(status_code=200, body=result)
            
        except ValueError as error:
            return self._handle_error(error)
        except Exception as error:
            return self._handle_error(error, 500) 