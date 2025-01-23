from abc import ABC, abstractmethod

class PollControllerInterface(ABC):
    @abstractmethod
    async def create_poll(self, poll_data: dict, token: str) -> dict:
        pass

    @abstractmethod
    async def vote(self, poll_id: str, option_index: int, token: str) -> dict:
        pass

    @abstractmethod
    async def get_poll(self, poll_id: str) -> dict:
        pass

    @abstractmethod
    async def list_polls(self, page: int = 1, limit: int = 10) -> list[dict]:
        pass

    @abstractmethod
    async def get_user_polls(self, token: str) -> list[dict]:
        pass 