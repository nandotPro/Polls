from .http_error import HttpError

class HttpUnprocessableEntityError(HttpError):
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422,
            name="Unprocessable Entity"
        ) 