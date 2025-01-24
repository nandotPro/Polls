import pytest
from unittest.mock import Mock, AsyncMock
from src.controllers.poll_controller import PollController

class TestPollController:
    def setup_method(self):
        # Criar mocks
        self.poll_repository = Mock()
        self.poll_cache_repository = Mock()
        self.auth_handler = Mock()

        # Configurar métodos assíncronos
        self.poll_repository.create_poll = AsyncMock()
        self.poll_repository.find_by_id = AsyncMock()
        self.poll_repository.increment_vote = AsyncMock()
        self.poll_cache_repository.has_user_voted = AsyncMock()
        self.poll_cache_repository.register_vote = AsyncMock()
        self.poll_cache_repository.get_poll_votes = AsyncMock()

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

    @pytest.mark.asyncio
    async def test_create_poll_success(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_repository.create_poll.return_value = "poll_id"

        # Act
        result = await self.poll_controller.create_poll(self.poll_data, "fake_token")

        # Assert
        assert result["poll_id"] == "poll_id"
        self.poll_repository.create_poll.assert_called_once()

    @pytest.mark.asyncio
    async def test_vote_success(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_cache_repository.has_user_voted.return_value = False
        self.poll_cache_repository.register_vote.return_value = True

        # Act
        result = await self.poll_controller.vote("poll_id", 0, "fake_token")

        # Assert
        assert result["message"] == "Voto registrado com sucesso"
        self.poll_repository.increment_vote.assert_called_once()

    @pytest.mark.asyncio
    async def test_vote_already_voted(self):
        # Arrange
        self.auth_handler.validate_token.return_value = "user_id"
        self.poll_cache_repository.has_user_voted.return_value = True

        # Act & Assert
        with pytest.raises(ValueError, match="Usuário já votou nesta enquete"):
            await self.poll_controller.vote("poll_id", 0, "fake_token")

    @pytest.mark.asyncio
    async def test_get_poll_success(self):
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
        result = await self.poll_controller.get_poll("poll123")

        # Assert
        assert result["_id"] == "poll123"
        assert result["options"][0]["votes"] == 5
        assert result["options"][1]["votes"] == 3
        self.poll_repository.find_by_id.assert_called_once_with("poll123")
        self.poll_cache_repository.get_poll_votes.assert_called_once_with("poll123")

    @pytest.mark.asyncio
    async def test_get_poll_not_found(self):
        # Arrange
        self.poll_repository.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Enquete não encontrada"):
            await self.poll_controller.get_poll("nonexistent123") 