from abc import ABC, abstractmethod
from ..http_types.http_request import HttpRequest
from ..http_types.http_response import HttpResponse

class ViewInterface(ABC):
    @abstractmethod
    async def handle(self, http_request: HttpRequest) -> HttpResponse:
        pass 