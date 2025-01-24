class HttpRequest:
    def __init__(self, headers: dict = None, body: dict = None, query_params: dict = None) -> None:
        self.headers = headers or {}
        self.body = body or {}
        self.query_params = query_params or {} 