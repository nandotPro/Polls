from .http_error import HttpError

class HttpBadRequestError(HttpError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=400,
            name="Bad Request"
        ) 