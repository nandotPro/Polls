from .http_error import HttpError

class HttpNotFoundError(HttpError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=404,
            name="Not Found"
        ) 