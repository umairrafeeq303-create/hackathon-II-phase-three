"""
Authentication API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select
from src.db.session import get_session
from src.models.user import User
from src.schemas.auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    AuthResponse,
)
from src.core.security import hash_password, verify_password, create_access_token
from src.core.deps import get_current_user_id

router = APIRouter()


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Create a new user account.

    Request Body:
        - name: User's full name (1-100 characters)
        - email: Valid email address (unique, lowercase)
        - password: Password (minimum 8 characters)

    Returns:
        - 201: AuthResponse with user data and JWT token
        - 400: Email already registered
        - 422: Validation error (invalid email, short password, etc.)

    Security:
        - Passwords are hashed using bcrypt with 10 rounds
        - Email is converted to lowercase for consistency
        - JWT token expires in 7 days
    """
    # Check if email already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    hashed_password = hash_password(user_data.password)

    # Create user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hashed_password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Generate JWT token
    token = create_access_token({"user_id": str(new_user.id)})

    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        token=token,
    )


@router.post("/signin", response_model=AuthResponse)
def signin(credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Sign in an existing user.

    Request Body:
        - email: User's email address
        - password: User's password

    Returns:
        - 200: AuthResponse with user data and JWT token
        - 401: Invalid credentials (wrong email or password)

    Security:
        - Timing attack prevention: Same error message for wrong email/password
        - Password verification using bcrypt
        - JWT token expires in 7 days
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == credentials.email)).first()

    # Timing attack prevention: verify password even if user not found
    if not user:
        # Perform dummy password check to maintain consistent timing
        hash_password("dummy_password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Verify password
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate JWT token
    token = create_access_token({"user_id": str(user.id)})

    # Return response
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=token,
    )


@router.get("/me", response_model=UserResponse)
def get_current_user(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Get current authenticated user's information.

    Headers:
        - Authorization: Bearer <jwt_token>

    Returns:
        - 200: UserResponse with user data
        - 401: Invalid or expired token
        - 404: User not found

    Security:
        - Requires valid JWT token in Authorization header
        - Extracts user_id from token payload
        - Validates user still exists in database
    """
    # Find user by ID from token
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse.model_validate(user)
