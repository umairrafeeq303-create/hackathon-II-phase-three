"""
Pydantic schemas for authentication requests and responses.
"""
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Validation:
        - email: Valid email format
        - name: 1-100 characters
        - password: Minimum 8 characters
    """

    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        """Convert email to lowercase for consistent storage."""
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Validation:
        - email: Valid email format
        - password: Not empty
    """

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")

    @field_validator("email")
    @classmethod
    def email_lowercase(cls, v: str) -> str:
        """Convert email to lowercase for consistent lookup."""
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "SecurePass123!",
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.
    Excludes sensitive fields like hashed_password.
    """

    id: UUID = Field(..., description="User's unique identifier")
    email: str = Field(..., description="User's email address")
    name: str = Field(..., description="User's full name")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john@example.com",
                "name": "John Doe",
                "created_at": "2026-01-09T10:30:00Z",
            }
        }


class AuthResponse(BaseModel):
    """
    Schema for authentication response (signup/signin).
    Contains user data and JWT token.
    """

    user: UserResponse = Field(..., description="User information")
    token: str = Field(..., description="JWT authentication token")

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "john@example.com",
                    "name": "John Doe",
                    "created_at": "2026-01-09T10:30:00Z",
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            }
        }


class TokenPayload(BaseModel):
    """
    Schema for JWT token payload.
    """

    user_id: str = Field(..., description="User ID encoded in token")
    exp: int = Field(..., description="Token expiration timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "exp": 1736510400,
            }
        }
