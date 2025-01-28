from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

class PollValidator():
    @staticmethod
    def validate_fields(request_body: dict, required_fields: list[str]) -> None:
        if not request_body:
            raise HttpBadRequestError("Body é obrigatório")

        for field in required_fields:
            if field not in request_body or request_body[field] is None:
                raise HttpBadRequestError(f"Campo {field} é obrigatório")

    def validate_create_poll(self, request: HttpRequest) -> None:
        required_fields = ["title", "options"]
        self.validate_fields(request.body, required_fields)

        if not isinstance(request.body["options"], list):
            raise HttpUnprocessableEntityError("Options deve ser uma lista")
        
        if len(request.body["options"]) < 2:
            raise HttpUnprocessableEntityError("Enquete deve ter pelo menos 2 opções")

        for option in request.body["options"]:
            if not isinstance(option, dict) or "text" not in option:
                raise HttpUnprocessableEntityError("Cada opção deve ter um campo 'text'")
            if not option["text"]:
                raise HttpBadRequestError("Texto da opção não pode ser vazio")

    def validate_vote(self, request: HttpRequest) -> None:
        required_fields = ["poll_id", "option_index"]
        self.validate_fields(request.body, required_fields)

        if not isinstance(request.body["option_index"], int):
            raise HttpUnprocessableEntityError("option_index deve ser um número") 