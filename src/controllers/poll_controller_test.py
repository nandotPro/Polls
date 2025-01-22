import pytest
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from src.controllers.poll_controller import PollController
from src.models.mongodb.repository.poll_repository import PollRepository
from src.models.redis.repository.poll_cache_repository import PollCacheRepository

class TestPollController:
    def setup_method(self):
        # Criar mocks para os repositórios
        self.poll_repository_mock = Mock(spec=PollRepository)
        self.poll_cache_repository_mock = Mock(spec=PollCacheRepository)
        
        # Configurar métodos assíncronos
        self.poll_repository_mock.create_poll = AsyncMock()
        self.poll_repository_mock.find_by_id = AsyncMock()
        self.poll_repository_mock.increment_vote = AsyncMock()
        self.poll_cache_repository_mock.has_user_voted = AsyncMock()
        self.poll_cache_repository_mock.register_vote = AsyncMock()
        self.poll_cache_repository_mock.get_poll_votes = AsyncMock()

        # Criar controller com os mocks
        with patch('src.controllers.poll_controller.PollRepository', return_value=self.poll_repository_mock), \
             patch('src.controllers.poll_controller.PollCacheRepository', return_value=self.poll_cache_repository_mock):
            self.poll_controller = PollController()

        # Dados de teste
        self.test_token = "test.token.here"
        self.test_user_id = "user123"
        self.test_poll_data = {
            "title": "Test Poll",
            "options": [
                {"text": "Option 1"},
                {"text": "Option 2"}
            ]
        }

    @pytest.mark.asyncio
    async def test_create_poll_success(self):
        # Arrange
        self.poll_controller.auth_handler.validate_token = Mock(return_value=self.test_user_id)
        self.poll_repository_mock.create_poll.return_value = "poll123"

        # Act
        result = await self.poll_controller.create_poll(self.test_poll_data.copy(), self.test_token)

        # Assert
        assert result["poll_id"] == "poll123"
        created_poll = self.poll_repository_mock.create_poll.call_args[0][0]
        assert created_poll["created_by"] == self.test_user_id
        assert "created_at" in created_poll
        assert all(option["votes"] == 0 for option in created_poll["options"])
        self.poll_repository_mock.create_poll.assert_called_once()

    @pytest.mark.asyncio
    async def test_vote_success(self):
        # Arrange
        self.poll_controller.auth_handler.validate_token = Mock(return_value=self.test_user_id)
        self.poll_cache_repository_mock.has_user_voted.return_value = False
        self.poll_cache_repository_mock.register_vote.return_value = True
        self.poll_repository_mock.increment_vote.return_value = True

        # Act
        result = await self.poll_controller.vote("poll123", 0, self.test_token)

        # Assert
        assert result["message"] == "Voto registrado com sucesso"
        self.poll_cache_repository_mock.register_vote.assert_called_once_with("poll123", self.test_user_id, 0)
        self.poll_repository_mock.increment_vote.assert_called_once_with("poll123", 0)

    @pytest.mark.asyncio
    async def test_vote_already_voted(self):
        # Arrange
        self.poll_controller.auth_handler.validate_token = Mock(return_value=self.test_user_id)
        self.poll_cache_repository_mock.has_user_voted.return_value = True

        # Act & Assert
        with pytest.raises(ValueError, match="Usuário já votou nesta enquete"):
            await self.poll_controller.vote("poll123", 0, self.test_token)

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
        self.poll_repository_mock.find_by_id.return_value = test_poll
        self.poll_cache_repository_mock.get_poll_votes.return_value = {"option:0": 5, "option:1": 3}

        # Act
        result = await self.poll_controller.get_poll("poll123")

        # Assert
        assert result["_id"] == "poll123"
        assert result["options"][0]["votes"] == 5
        assert result["options"][1]["votes"] == 3
        self.poll_repository_mock.find_by_id.assert_called_once_with("poll123")
        self.poll_cache_repository_mock.get_poll_votes.assert_called_once_with("poll123")

    @pytest.mark.asyncio
    async def test_get_poll_not_found(self):
        # Arrange
        self.poll_repository_mock.find_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Enquete não encontrada"):
            await self.poll_controller.get_poll("nonexistent123") 