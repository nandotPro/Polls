from src.views.http_types.http_request import HttpRequest

class AuthValidator():
    @staticmethod
    def validate_fields(request_body: dict, required_fields: list[str]) -> None:
        if not request_body:
            raise ValueError("Body é obrigatório")

        for field in required_fields:
            if not request_body.get(field):
                raise ValueError(f"Campo {field} é obrigatório")
            if not isinstance(request_body[field], str):
                raise ValueError(f"Campo {field} deve ser uma string")

    def validate_register(self, request: HttpRequest) -> None:
        required_fields = ["username", "email", "password"]
        self.validate_fields(request.body, required_fields)

        if not "@" in request.body["email"]:
            raise ValueError("Email inválido")
        if len(request.body["password"]) < 6:
            raise ValueError("Senha deve ter no mínimo 6 caracteres")

    def validate_login(self, request: HttpRequest) -> None:
        required_fields = ["email", "password"]
        self.validate_fields(request.body, required_fields) 