import hmac
import os

from fastapi import Header, HTTPException, status


READER_API_KEY = os.getenv("READER_API_KEY")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")


def _keys_match(provided_key: str, expected_key: str | None) -> bool:
    """Compare API keys safely."""

    if not expected_key:
        return False

    return hmac.compare_digest(
        provided_key,
        expected_key
    )


def require_reader(
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Allow reader or administrator access."""

    if (
        _keys_match(x_api_key, READER_API_KEY)
        or _keys_match(x_api_key, ADMIN_API_KEY)
    ):
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key."
    )


def require_admin(
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Allow administrator access only."""

    if _keys_match(x_api_key, ADMIN_API_KEY):
        return True

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Administrator access required."
    )
