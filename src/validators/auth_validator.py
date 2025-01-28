from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

class AuthValidator():
    @staticmethod
    def validate_fields(request_body: dict, required_fields: list[str]) -> None:
        if not request_body:
            raise HttpBadRequestError("Body é obrigatório")

        for field in required_fields:
            if not request_body.get(field):
                raise HttpBadRequestError(f"Campo {field} é obrigatório")
            if not isinstance(request_body[field], str):
                raise HttpUnprocessableEntityError(f"Campo {field} deve ser uma string")

    def validate_register(self, request: HttpRequest) -> None:
        required_fields = ["username", "email", "password"]
        self.validate_fields(request.body, required_fields)

        if not "@" in request.body["email"]:
            raise HttpUnprocessableEntityError("Email inválido")
        if len(request.body["password"]) < 6:
            raise HttpUnprocessableEntityError("Senha deve ter no mínimo 6 caracteres")

    def validate_login(self, request: HttpRequest) -> None:
        required_fields = ["email", "password"]
        self.validate_fields(request.body, required_fields) 