from abc import ABC, abstractmethod
from typing import Dict

class PollCacheRepositoryInterface(ABC):
    @abstractmethod
    def register_vote(self, poll_id: str, user_id: str, option_index: int) -> bool:
        """Registra o voto de um usuário em uma enquete"""
        pass

    @abstractmethod
    def get_poll_votes(self, poll_id: str) -> Dict:
        """Retorna a contagem de votos de uma enquete"""
        pass

    @abstractmethod
    def has_user_voted(self, poll_id: str, user_id: str) -> bool:
        """Verifica se um usuário já votou em uma enquete"""
        pass

    @abstractmethod
    def delete_poll_votes(self, poll_id: str) -> None:
        """Remove todos os votos de uma enquete"""
        pass 