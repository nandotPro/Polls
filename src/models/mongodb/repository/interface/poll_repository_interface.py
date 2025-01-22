from abc import ABC, abstractmethod
from typing import Optional, List, Dict

class PollRepositoryInterface(ABC):
    @abstractmethod
    def create_poll(self, poll_data: dict) -> str:
        """Cria uma nova enquete"""
        pass

    @abstractmethod
    def find_by_id(self, poll_id: str) -> Optional[dict]:
        """Busca uma enquete pelo ID"""
        pass

    @abstractmethod
    def find_all_polls(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Retorna uma lista de enquetes com paginação"""
        pass

    @abstractmethod
    def find_user_polls(self, user_id: str) -> List[dict]:
        """Retorna todas as enquetes de um usuário"""
        pass

    @abstractmethod
    def delete_poll(self, poll_id: str) -> bool:
        """Remove uma enquete"""
        pass

    @abstractmethod
    def increment_vote(self, poll_id: str, option_index: int) -> bool:
        """Incrementa o contador de votos de uma opção"""
        pass 