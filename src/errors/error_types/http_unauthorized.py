from .http_error import HttpError

class HttpUnauthorizedError(HttpError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=401,
            name="Unauthorized"
        ) 