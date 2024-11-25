from fastapi import HTTPException, status


class OrdersException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class SpecialistBusyException(OrdersException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Specialist is busy at the time"


class WrongTimeException(OrdersException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect time format, example: 2024-10-18T15:38:45"


class NoSuchOrderException(OrdersException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such order"


class RateLimitException(OrdersException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Rate limit exceeded"


class NoSuchSpecialistException(OrdersException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such specialist"
