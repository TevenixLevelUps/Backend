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

    havent_reset_request = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Have not reset request",
    )

    code_expired = HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="Code expired",
    )
    too_many_requests = HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail="Too many requests",
    )

    active_request = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="You also have active requests with active code",
    )
