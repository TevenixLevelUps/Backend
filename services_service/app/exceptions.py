from fastapi import HTTPException, status


class ServicesException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoSuchServiceException(ServicesException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such service"


class NoSuchServiceImageException(ServicesException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such service image"


class NotImageException(ServicesException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    detail = "Uploaded file is not an image"


class ImageForThisServiceAlreadyExistsException(ServicesException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This service already has a picture"


class ServiceAlreadyExistsException(ServicesException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This service already exists"


class RateLimitException(ServicesException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Rate limit exceeded"
