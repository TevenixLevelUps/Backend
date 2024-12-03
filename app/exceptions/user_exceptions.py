from fastapi import HTTPException, status


class UserHTTPException:
    email_already_registered = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already registered",
    )
    invalid_confirmation_code = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid confirmation code",
    )
    incorrect_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email_not_confirmed = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email not confirmed",
        headers={"WWW-Authenticate": "Bearer"},
    )
    not_logged_in = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not logged in",
    )

    email_not_registered = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email not registered",
    )
