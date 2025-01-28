import pytest
from src.validators.poll_validator import PollValidator
from src.views.http_types.http_request import HttpRequest
from src.errors.error_types.http_bad_request import HttpBadRequestError
from src.errors.error_types.http_unprocessable_entity import HttpUnprocessableEntityError

class TestPollValidator:
    def setup_method(self):
        self.validator = PollValidator()
        self.valid_create_request = HttpRequest(
            body={
                "title": "Test Poll",
                "options": [
                    {"text": "Option 1"},
                    {"text": "Option 2"}
                ]
            }
        )
        self.valid_vote_request = HttpRequest(
            body={
                "poll_id": "123",
                "option_index": 0
            }
        )

    def test_validate_create_poll_success(self):
        # Act & Assert
        self.validator.validate_create_poll(self.valid_create_request)  # Não deve lançar exceção

    def test_validate_create_poll_missing_body(self):
        # Arrange
        request = HttpRequest()

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Body é obrigatório"):
            self.validator.validate_create_poll(request)

    def test_validate_create_poll_missing_field(self):
        # Arrange
        request = HttpRequest(body={"title": "Test Poll"})

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Campo options é obrigatório"):
            self.validator.validate_create_poll(request)

    def test_validate_create_poll_invalid_options_type(self):
        # Arrange
        request = HttpRequest(
            body={
                "title": "Test Poll",
                "options": "not a list"
            }
        )

        # Act & Assert
        with pytest.raises(HttpUnprocessableEntityError, match="Options deve ser uma lista"):
            self.validator.validate_create_poll(request)

    def test_validate_create_poll_insufficient_options(self):
        # Arrange
        request = HttpRequest(
            body={
                "title": "Test Poll",
                "options": [{"text": "Option 1"}]
            }
        )

        # Act & Assert
        with pytest.raises(HttpUnprocessableEntityError, match="Enquete deve ter pelo menos 2 opções"):
            self.validator.validate_create_poll(request)

    def test_validate_create_poll_invalid_option_format(self):
        # Arrange
        request = HttpRequest(
            body={
                "title": "Test Poll",
                "options": [
                    {"text": "Option 1"},
                    "invalid option"
                ]
            }
        )

        # Act & Assert
        with pytest.raises(HttpUnprocessableEntityError, match="Cada opção deve ter um campo 'text'"):
            self.validator.validate_create_poll(request)

    def test_validate_vote_success(self):
        # Act & Assert
        self.validator.validate_vote(self.valid_vote_request)  # Não deve lançar exceção

    def test_validate_vote_missing_field(self):
        # Arrange
        request = HttpRequest(body={"poll_id": "123"})

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Campo option_index é obrigatório"):
            self.validator.validate_vote(request)

    def test_validate_vote_invalid_option_index_type(self):
        # Arrange
        request = HttpRequest(
            body={
                "poll_id": "123",
                "option_index": "0"  # deveria ser int
            }
        )

        # Act & Assert
        with pytest.raises(HttpUnprocessableEntityError, match="option_index deve ser um número"):
            self.validator.validate_vote(request) 