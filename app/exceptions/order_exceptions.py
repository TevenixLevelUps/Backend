from fastapi import HTTPException, status


class OrderHTTPException:
    service_or_specialist_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Service or specialist not found",
    )
    specialist_not_available = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Specialist is not available at this time",
    )
    order_not_found = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Order not found",
    )
