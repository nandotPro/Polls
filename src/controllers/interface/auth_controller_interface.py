from abc import ABC, abstractmethod

class AuthControllerInterface(ABC):
    @abstractmethod
    async def register(self, user_data: dict) -> dict:
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> dict:
        pass 