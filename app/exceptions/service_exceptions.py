from fastapi import HTTPException, status


class ServiceHTTPException:
    service_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Service not found",
    )
    invalid_service_data = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid service data provided",
    )
    service_creation_failed = HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to create service",
    )
