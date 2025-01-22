from abc import ABC, abstractmethod
from typing import Optional

class UserRepositoryInterface(ABC):
    @abstractmethod
    def register_user(self, user_data: dict) -> str:
        """Registra um novo usuário"""
        pass

    @abstractmethod
    def login_user(self, email: str, password_hash: str) -> Optional[dict]:
        """Realiza o login do usuário"""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[dict]:
        """Busca um usuário pelo email"""
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[dict]:
        """Busca um usuário pelo ID"""
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[dict]:
        """Busca um usuário pelo nome de usuário"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> bool:
        """Remove um usuário"""
        pass 