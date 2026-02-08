"""
Security utilities for password hashing and JWT token management.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from src.core.config import settings


def hash_password(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Note:
        bcrypt has a maximum password length of 72 bytes. Passwords are
        automatically truncated to 72 bytes before hashing to prevent errors.
    """
    # Truncate to 72 bytes to comply with bcrypt's limit
    password_bytes = password.encode("utf-8")[:72]

    # Generate salt and hash the password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return as string
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise

    Note:
        Passwords are truncated to 72 bytes before verification to match
        the hashing behavior and ensure consistency.
    """
    # Truncate to 72 bytes to match hashing behavior
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode in the token (should include 'user_id')
        expires_delta: Optional expiration time delta (defaults to JWT_EXPIRATION_DAYS)

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.JWT_EXPIRATION_DAYS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.BETTER_AUTH_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload as dictionary, or None if invalid
    """
    try:
        payload = jwt.decode(
            token, settings.BETTER_AUTH_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
