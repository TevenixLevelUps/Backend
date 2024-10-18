from fastapi import HTTPException, status


class BarberShopException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoSuchServiceException(BarberShopException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such service"


class NoSuchServiceImageException(BarberShopException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such service image"


class NotImageException(BarberShopException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    detail = "Uploaded file is not an image"


class ImageForThisServiceAlreadyExistsException(BarberShopException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This service already has a picture"


class ServiceAlreadyExistsException(BarberShopException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This service already exists"


class NoSuchSpecialistException(BarberShopException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such specialist"


class SpecialistAlreadyExistsException(BarberShopException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This specialist already exists"


class NoSuchSpecialistAvatarException(BarberShopException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such specialist avatar"


class AvatarForThisSpecialistAlreadyExistsException(BarberShopException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This specialist already has an avatar"


class SpecialistBusyException(BarberShopException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Specialist is busy at the time"


class WrongTimeException(BarberShopException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Incorrect time format, example: 2024-10-18T15:38:45"


class NoSuchOrderException(BarberShopException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "There is no such order"
