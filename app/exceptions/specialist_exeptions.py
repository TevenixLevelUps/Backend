from fastapi import HTTPException, status


class SpecialistHTTPException:
    specialist_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Specialist not found",
    )
    avatar_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Avatar not found",
    )
    invalid_specialist_data = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid specialist data provided",
    )
    specialist_creation_failed = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create specialist",
    )
