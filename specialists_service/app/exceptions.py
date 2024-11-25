from fastapi import HTTPException, status


class SpecialistsException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoSuchSpecialistException(SpecialistsException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such specialist"


class SpecialistAlreadyExistsException(SpecialistsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This specialist already exists"


class NotImageException(SpecialistsException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    detail = "Uploaded file is not an image"


class NoSuchSpecialistAvatarException(SpecialistsException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such specialist avatar"


class AvatarForThisSpecialistAlreadyExistsException(SpecialistsException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This specialist already has an avatar"


class RateLimitException(SpecialistsException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Rate limit exceeded"
