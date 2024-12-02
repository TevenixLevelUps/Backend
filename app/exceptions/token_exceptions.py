from fastapi import HTTPException, status


class TokenHTTPException:
    verify_token_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Exception in verify_token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    decode_error = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Error in decode",
    )
    db_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error in db request",
    )
    token_not_found_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error, token not found",
    )
    expired_token_error = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Error, expired token",
    )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    admin_role_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perform this action",
    )
