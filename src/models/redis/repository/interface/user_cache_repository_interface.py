from abc import ABC, abstractmethod
from typing import Optional

class UserCacheRepositoryInterface(ABC):
    @abstractmethod
    def set_user(self, user_id: str, user_data: dict) -> None:
        """Armazena dados do usuário em cache"""
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[dict]:
        """Recupera dados do usuário do cache"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        """Remove dados do usuário do cache"""
        pass 