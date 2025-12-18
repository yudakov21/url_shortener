from fastapi import status


class ShortenerBaseException(Exception):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad request"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)


class NotLongUrlException(ShortenerBaseException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Url was not found!!!"