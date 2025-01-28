import pytest
from unittest.mock import Mock
from src.controllers.poll_controller import PollController
from src.errors.error_types.http_unauthorized import HttpUnauthorizedError
from src.errors.error_types.http_not_found import HttpNotFoundError
from src.errors.error_types.http_bad_request import HttpBadRequestError

class TestPollController:
    def setup_method(self):
        # Criar mocks
        self.poll_repository = Mock()
        self.poll_cache_repository = Mock()
        self.auth_handler = Mock()

        # Configurar métodos
        self.poll_repository.create_poll = Mock()
        self.poll_repository.find_by_id = Mock()
        self.poll_repository.increment_vote = Mock()
        self.poll_cache_repository.has_user_voted = Mock()
        self.poll_cache_repository.register_vote = Mock()
        self.poll_cache_repository.get_poll_votes = Mock()

        # Configurar controller com mocks
        self.poll_controller = PollController(
            poll_repository=self.poll_repository,
            poll_cache_repository=self.poll_cache_repository,
            auth_handler=self.auth_handler
        )

        # Dados de teste
        self.poll_data = {
            "title": "Test Poll",
            "options": [
                {"text": "Option 1"},
                {"text": "Option 2"}
            ]
        }

    def test_create_poll_success(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_repository.create_poll.return_value = "poll_id"

        # Act
        result = self.poll_controller.create_poll(self.poll_data, "fake_token")

        # Assert
        assert result["poll_id"] == "poll_id"
        self.poll_repository.create_poll.assert_called_once()

    def test_vote_success(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_cache_repository.has_user_voted.return_value = False
        self.poll_cache_repository.register_vote.return_value = True

        # Act
        result = self.poll_controller.vote("poll_id", 0, "fake_token")

        # Assert
        assert result["message"] == "Voto registrado com sucesso"
        self.poll_repository.increment_vote.assert_called_once()

    def test_vote_already_voted(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_cache_repository.has_user_voted.return_value = True

        # Act & Assert
        with pytest.raises(HttpBadRequestError, match="Usuário já votou nesta enquete"):
            self.poll_controller.vote("poll_id", 0, "fake_token")

    def test_get_poll_success(self):
        # Arrange
        test_poll = {
            "_id": "poll123",
            "title": "Test Poll",
            "options": [
                {"text": "Option 1", "votes": 0},
                {"text": "Option 2", "votes": 0}
            ]
        }
        self.poll_repository.find_by_id.return_value = test_poll
        self.poll_cache_repository.get_poll_votes.return_value = {"option:0": 5, "option:1": 3}

        # Act
        result = self.poll_controller.get_poll("poll123")

        # Assert
        assert result["_id"] == "poll123"
        assert result["options"][0]["votes"] == 5
        assert result["options"][1]["votes"] == 3
        self.poll_repository.find_by_id.assert_called_once_with("poll123")
        self.poll_cache_repository.get_poll_votes.assert_called_once_with("poll123")

    def test_get_poll_not_found(self):
        # Arrange
        self.poll_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HttpNotFoundError, match="Enquete não encontrada"):
            self.poll_controller.get_poll("nonexistent123")

    def test_invalid_token(self):
        # Arrange
        self.auth_handler.validate_token.side_effect = HttpUnauthorizedError("Token inválido")

        # Act & Assert
        with pytest.raises(HttpUnauthorizedError, match="Token inválido"):
            self.poll_controller.create_poll(self.poll_data, "invalid_token")

    def test_list_polls_success(self):
        # Arrange
        test_polls = [
            {
                "_id": "poll1",
                "title": "Test Poll 1",
                "options": [{"text": "Option 1", "votes": 0}]
            },
            {
                "_id": "poll2",
                "title": "Test Poll 2",
                "options": [{"text": "Option 1", "votes": 0}]
            }
        ]
        self.poll_repository.find_all_polls.return_value = test_polls

        # Act
        result = self.poll_controller.list_polls(page=1, limit=10)

        # Assert
        assert len(result) == 2
        assert result[0]["_id"] == "poll1"
        self.poll_repository.find_all_polls.assert_called_once_with(0, 10)

    def test_get_user_polls_success(self):
        # Arrange
        test_polls = [
            {
                "_id": "poll1",
                "title": "User Poll 1",
                "created_by": "user123"
            }
        ]
        self.auth_handler.validate_token.return_value = "user123"
        self.poll_repository.find_user_polls.return_value = test_polls

        # Act
        result = self.poll_controller.get_user_polls("fake_token")

        # Assert
        assert len(result) == 1
        assert result[0]["_id"] == "poll1"
        self.poll_repository.find_user_polls.assert_called_once_with("user123") 