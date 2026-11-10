"""Ожидаемые ошибки домена; HTTP-представление задаётся в API."""


class GeneAnalysisError(Exception):
    def __init__(self, message: str, status_code: int = 422):
        super().__init__(message)
        self.status_code = status_code
