from httpx import Response


class ApiException(Exception):
    def __init__(self, response: Response):
        self.status_code = response.status_code
        self.headers = response.headers
        self.text = response.text

        message = f"HTTP {self.status_code} - {self.text}"
        if len(message) > 1000:
            message = message[:1000] + "..."
        super().__init__(message)


class AppNotFound(Exception):
    pass


class AuthenticationError(ApiException):
    pass


class NoReleaseFound(Exception):
    pass


class VersionNotFound(Exception):
    pass
