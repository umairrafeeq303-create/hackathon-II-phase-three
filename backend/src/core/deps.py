"""
FastAPI dependencies for authentication and authorization.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from src.core.security import decode_access_token
from src.db.session import get_session

# HTTP Bearer token scheme for Authorization header
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Extract and validate user_id from JWT token in Authorization header.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        user_id (UUID string) from token payload

    Raises:
        HTTPException: 401 if token is invalid, expired, or missing user_id
    """
    token = credentials.credentials

    # Decode and verify token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from payload
    user_id: Optional[str] = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def get_current_user_id_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    ),
) -> Optional[str]:
    """
    Extract user_id from JWT token if present, or return None.
    Useful for endpoints that have optional authentication.

    Args:
        credentials: Optional HTTP Bearer credentials

    Returns:
        user_id (UUID string) if valid token present, None otherwise
    """
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        return None

    return payload.get("user_id")
