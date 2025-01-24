from src.models.redis.repository.interface.poll_cache_repository_interface import PollCacheRepositoryInterface

class PollCacheRepository(PollCacheRepositoryInterface):
    def __init__(self, redis_connection):
        self.redis = redis_connection
        self.EXPIRE_TIME = 3600  # 1 hora em segundos

    def register_vote(self, poll_id: str, user_id: str, option_index: int) -> bool:
        """
        Registra voto do usuário.
        Retorna False se usuário já votou nesta enquete.
        """
        vote_key = f"vote:{poll_id}:{user_id}"
        
        # Verifica se usuário já votou
        if self.redis.exists(vote_key):
            return False
        
        # Registra o voto
        pipeline = self.redis.pipeline()
        pipeline.hincrby(f"poll:{poll_id}", f"option:{option_index}", 1)
        pipeline.set(vote_key, option_index)
        pipeline.execute()
        
        return True

    def get_poll_votes(self, poll_id: str) -> dict:
        """Retorna contagem de votos em tempo real"""
        votes = self.redis.hgetall(f"poll:{poll_id}")
        return {k: int(v) for k, v in votes.items()}

    def has_user_voted(self, poll_id: str, user_id: str) -> bool:
        """Verifica se usuário já votou na enquete"""
        return self.redis.exists(f"vote:{poll_id}:{user_id}")

    def delete_poll_votes(self, poll_id: str) -> None:
        """Remove todos os dados de votação de uma enquete"""
        # Remove contagem de votos
        self.redis.delete(f"poll:{poll_id}")
        
        # Remove registros de votos de usuários
        pattern = f"vote:{poll_id}:*"
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)