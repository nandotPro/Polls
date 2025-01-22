from src.models.mongodb.repository.poll_repository import PollRepository
from src.models.redis.repository.poll_cache_repository import PollCacheRepository
from src.services.jwt_handler import JWTHandler
from datetime import datetime

class PollController:
    def __init__(self):
        self.poll_repository = PollRepository()
        self.poll_cache_repository = PollCacheRepository()
        self.auth_handler = JWTHandler()

    async def create_poll(self, poll_data: dict, token: str) -> dict:
        """Cria uma nova enquete"""
        # Validar token e obter user_id
        user_id = self.auth_handler.validate_token(token)
        
        # Preparar dados da enquete
        poll_data["created_by"] = user_id
        poll_data["created_at"] = datetime.now()
        for option in poll_data["options"]:
            option["votes"] = 0

        # Salvar enquete
        poll_id = await self.poll_repository.create_poll(poll_data)
        
        return {"poll_id": poll_id}

    async def get_poll(self, poll_id: str) -> dict:
        """Retorna dados de uma enquete com contagem de votos em tempo real"""
        # Buscar enquete
        poll = await self.poll_repository.find_by_id(poll_id)
        if not poll:
            raise ValueError("Enquete não encontrada")

        # Buscar votos em tempo real
        votes = await self.poll_cache_repository.get_poll_votes(poll_id)
        
        # Atualizar contagem de votos
        for option in poll["options"]:
            option_key = f"option:{poll['options'].index(option)}"
            option["votes"] = votes.get(option_key, 0)

        return poll

    async def vote(self, poll_id: str, option_index: int, token: str) -> dict:
        """Registra voto em uma enquete"""
        # Validar token e obter user_id
        user_id = self.auth_handler.validate_token(token)

        # Verificar se usuário já votou
        if await self.poll_cache_repository.has_user_voted(poll_id, user_id):
            raise ValueError("Usuário já votou nesta enquete")

        # Registrar voto no cache
        success = await self.poll_cache_repository.register_vote(poll_id, user_id, option_index)
        if not success:
            raise ValueError("Erro ao registrar voto")

        # Incrementar voto no MongoDB
        await self.poll_repository.increment_vote(poll_id, option_index)

        return {"message": "Voto registrado com sucesso"}

    async def list_polls(self, page: int = 1, limit: int = 10) -> list[dict]:
        """Lista enquetes com paginação"""
        skip = (page - 1) * limit
        return await self.poll_repository.find_all_polls(skip, limit)

    async def get_user_polls(self, token: str) -> list[dict]:
        """Lista enquetes criadas pelo usuário"""
        user_id = self.auth_handler.validate_token(token)
        return await self.poll_repository.find_user_polls(user_id) 