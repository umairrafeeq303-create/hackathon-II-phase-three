# Data Model: Authentication & User Management System

**Feature**: 001-auth
**Date**: 2026-01-09
**Phase**: 1 (Design)

## Overview

This document defines the data model for the Authentication & User Management System using SQLModel ORM with Neon PostgreSQL. The model implements the database schema specified in `spec.md` with production-ready patterns for FastAPI backend.

## User Model (Backend - SQLModel)

### Table Definition

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    """
    User model representing authenticated users in the todo application.

    This model stores user authentication credentials and profile information.
    Passwords are always stored as bcrypt hashes (never plain-text).
    """
    __tablename__ = "users"

    # Primary Key - UUID for security (prevents enumeration attacks)
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False
    )

    # Authentication Fields
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="User's email address (unique identifier for login)"
    )

    hashed_password: str = Field(
        max_length=60,  # Bcrypt hash output is always 60 characters
        nullable=False,
        description="Bcrypt hashed password (never store plain-text)"
    )

    # Profile Fields
    name: str = Field(
        max_length=100,
        nullable=False,
        description="User's display name"
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Account creation timestamp (UTC)"
    )

    class Config:
        schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john.doe@example.com",
                "name": "John Doe",
                "hashed_password": "$2b$10$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFG",
                "created_at": "2026-01-09T10:30:00Z"
            }
        }
```

### Field Specifications

| Field | Type | Constraints | Purpose |
|-------|------|-------------|---------|
| `id` | UUID | Primary Key, Not Null, Indexed | Unique user identifier (v4 UUID) |
| `email` | String(255) | Unique, Not Null, Indexed | User's email address for login |
| `hashed_password` | String(60) | Not Null | Bcrypt hash of user's password |
| `name` | String(100) | Not Null | User's display name |
| `created_at` | DateTime | Not Null, Default: utcnow | Account creation timestamp |

### Indexes

1. **Primary Index**: `id` (automatic primary key index)
2. **Unique Index**: `email` (enforces uniqueness, optimizes signin queries)

**Rationale**: Email index critical for signin performance (WHERE email = ?) and uniqueness enforcement.

### Constraints

1. **Unique Constraint**: `email` must be unique across all records
   - Enforced at database level (race condition protection)
   - Prevents duplicate account creation

2. **NOT NULL Constraints**: All fields are required
   - Ensures data integrity
   - Prevents partial user records

3. **Length Constraints**:
   - `email`: Maximum 255 characters (RFC 5322 email length limit)
   - `name`: Maximum 100 characters (reasonable display name length)
   - `hashed_password`: Exactly 60 characters (bcrypt output format)

## Pydantic Schemas (Request/Response Models)

### User Response Schema

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID

class UserResponse(BaseModel):
    """
    User response schema for API responses.
    Excludes hashed_password field for security.
    """
    id: UUID
    email: EmailStr
    name: str
    created_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel conversion
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john.doe@example.com",
                "name": "John Doe",
                "created_at": "2026-01-09T10:30:00Z"
            }
        }
```

**Security Note**: `hashed_password` is NEVER included in response schemas.

### User Create Schema (Signup)

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
import re

class UserCreate(BaseModel):
    """
    User creation schema for signup requests.
    Validates input before database insertion.
    """
    email: EmailStr = Field(
        description="User's email address (must be valid format)",
        examples=["john.doe@example.com"]
    )

    password: str = Field(
        min_length=8,
        description="User's password (minimum 8 characters)",
        examples=["SecurePass123!"]
    )

    name: str = Field(
        min_length=1,
        max_length=100,
        description="User's display name",
        examples=["John Doe"]
    )

    @field_validator('email')
    def validate_email_format(cls, v):
        """Validate email format using Pydantic EmailStr"""
        # EmailStr automatically validates RFC 5322 format
        return v.lower()  # Normalize to lowercase

    @field_validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets minimum requirements"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        # Additional validation can be added here if needed
        return v

    @field_validator('name')
    def validate_name(cls, v):
        """Validate name is not empty or whitespace-only"""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!",
                "name": "John Doe"
            }
        }
```

### User Login Schema (Signin)

```python
from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    """
    User login schema for signin requests.
    Simpler than UserCreate (no name field).
    """
    email: EmailStr = Field(
        description="User's registered email address",
        examples=["john.doe@example.com"]
    )

    password: str = Field(
        description="User's password",
        examples=["SecurePass123!"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123!"
            }
        }
```

### Authentication Response Schema

```python
from pydantic import BaseModel

class AuthResponse(BaseModel):
    """
    Authentication response schema for signup and signin.
    Returns user information and JWT token.
    """
    user: UserResponse
    token: str = Field(
        description="JWT access token (valid for 7 days)",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "email": "john.doe@example.com",
                    "name": "John Doe",
                    "created_at": "2026-01-09T10:30:00Z"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTczNjUwMDIwMCwiaWF0IjoxNzM1ODk1NDAwfQ.signature_here"
            }
        }
```

## JWT Token Payload Model

### Token Payload Schema

```python
from pydantic import BaseModel
from uuid import UUID

class TokenPayload(BaseModel):
    """
    JWT token payload structure.
    This is NOT stored in database - it's embedded in JWT tokens.
    """
    user_id: UUID = Field(
        description="User's unique identifier"
    )

    email: str = Field(
        description="User's email address (for UI context)"
    )

    exp: int = Field(
        description="Expiration timestamp (Unix epoch, 7 days from iat)"
    )

    iat: int = Field(
        description="Issued at timestamp (Unix epoch, current time)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "john.doe@example.com",
                "exp": 1736500200,
                "iat": 1735895400
            }
        }
```

**Token Details**:
- Algorithm: HS256 (HMAC-SHA256)
- Secret: `BETTER_AUTH_SECRET` environment variable
- Expiry: 7 days (604800 seconds) from issuance
- Format: `<header>.<payload>.<signature>` (Base64-encoded)

## Database Migrations

### Initial Migration (Alembic)

```python
"""Create users table

Revision ID: 001_create_users
Revises:
Create Date: 2026-01-09

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = '001_create_users'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False, index=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('hashed_password', sa.String(60), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('now()')),
    )

    # Create unique index on email (in addition to unique constraint)
    op.create_index('idx_users_email', 'users', ['email'], unique=True)

def downgrade():
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

**Migration Notes**:
- UUID type uses PostgreSQL native UUID type via SQLAlchemy
- `created_at` has server-side default (database handles timestamp)
- Email index created explicitly for query performance
- Downgrade path provided for rollback capability

## Data Validation Rules

### Email Validation

1. **Format**: RFC 5322 compliant email address
2. **Normalization**: Converted to lowercase before storage
3. **Uniqueness**: Checked at database level (unique constraint)
4. **Length**: Maximum 255 characters

**Implementation**: Pydantic `EmailStr` type handles RFC 5322 validation automatically.

### Password Validation

1. **Minimum Length**: 8 characters (enforced in UserCreate schema)
2. **Storage**: Always hashed with bcrypt (10+ salt rounds)
3. **Security**: Never logged, never stored plain-text, never returned in responses
4. **Special Characters**: All printable characters allowed (bcrypt handles them)

### Name Validation

1. **Minimum Length**: 1 character (non-empty)
2. **Maximum Length**: 100 characters
3. **Whitespace**: Leading/trailing whitespace trimmed
4. **Empty Check**: Whitespace-only names rejected

### UUID Validation

1. **Format**: Valid UUID v4 format
2. **Generation**: Automatic via `uuid4()` factory
3. **Uniqueness**: Guaranteed by UUID specification (collision probability negligible)

## Data Access Patterns

### Common Queries

**1. Find User by Email** (Signin)
```python
user = session.exec(
    select(User).where(User.email == email)
).first()
```
**Performance**: O(1) lookup via email index

**2. Find User by ID** (Get Current User)
```python
user = session.get(User, user_id)
```
**Performance**: O(1) lookup via primary key

**3. Create User** (Signup)
```python
user = User(
    email=user_create.email,
    name=user_create.name,
    hashed_password=hash_password(user_create.password)
)
session.add(user)
session.commit()
session.refresh(user)
```
**Concurrency**: Unique constraint on email prevents race conditions

**4. Check Email Existence** (Duplicate Prevention)
```python
existing_user = session.exec(
    select(User).where(User.email == email)
).first()
if existing_user:
    raise ValueError("Email already registered")
```
**Performance**: O(1) lookup via email index

## Security Considerations

### Password Storage

- **Never Store Plain-Text**: Passwords always hashed before database insertion
- **Bcrypt Algorithm**: Industry standard, designed for password hashing
- **Salt Rounds**: Minimum 10 (configurable via environment)
- **Hash Output**: Always 60 characters (bcrypt format)

### Sensitive Data Exclusion

- **API Responses**: `hashed_password` field NEVER included
- **Logs**: Plain-text passwords NEVER logged
- **Error Messages**: Generic messages prevent user enumeration

### Database Security

- **SQL Injection**: Prevented via SQLModel parameterized queries
- **Connection String**: Stored in `DATABASE_URL` environment variable
- **Unique Constraints**: Enforced at database level (race condition protection)

## Integration Points

### With Spec 2 (Task API)

**User ID Propagation**:
- Task model will have `user_id: UUID` foreign key referencing `users.id`
- Foreign key constraint ensures referential integrity
- Cascade delete: When user deleted, all their tasks deleted (TBD in Spec 2)

**Query Pattern**:
```python
# Task model will reference User
class Task(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    # ... other fields
```

### With Frontend (Spec 3)

**TypeScript Interfaces**:
- Frontend will define matching TypeScript interfaces for API contracts
- Type safety ensures request/response consistency
- Example: `interface User { id: string; email: string; name: string; created_at: string; }`

**API Client**:
- Frontend API client will use schemas for type checking
- Automatic JSON serialization/deserialization
- Error handling based on status codes

## Performance Characteristics

### Database Indexes

| Index | Type | Cardinality | Query Pattern | Estimated Performance |
|-------|------|-------------|---------------|----------------------|
| `id` (PK) | B-tree | High (UUID) | `WHERE id = ?` | O(log n) ≈ O(1) for primary key |
| `email` | B-tree, Unique | High | `WHERE email = ?` | O(log n) ≈ O(1) for unique index |

### Query Performance Expectations

- **Signin** (email lookup): <10ms at 100K users, <50ms at 1M users
- **Get User** (ID lookup): <5ms at any scale (primary key)
- **Create User**: <20ms (includes bcrypt hashing overhead of 300-500ms)
- **Check Duplicate**: <10ms (email index lookup)

### Scalability Notes

- **Connection Pooling**: SQLModel/SQLAlchemy manages pool automatically
- **Read Replicas**: Not needed for Phase II (single database sufficient)
- **Caching**: Not needed (queries are fast enough with indexes)
- **Partitioning**: Not needed (expected user count <100K)

## Data Model Checklist

- [x] User table defined with all required fields
- [x] UUID primary key for security
- [x] Email uniqueness constraint at database level
- [x] Email index for signin performance
- [x] Bcrypt password hashing enforced
- [x] Request/response schemas defined
- [x] Pydantic validation for all input fields
- [x] Security: hashed_password never in responses
- [x] JWT token payload structure defined
- [x] Database migration script provided
- [x] Integration points documented
- [x] Performance characteristics analyzed
