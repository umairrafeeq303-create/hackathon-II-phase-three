# Auth Agent Skills

## 1. FastAPI Security
- OAuth2PasswordBearer for token extraction
- JWT token generation and verification
- Security dependencies for protected routes
- HTTPException for auth errors

## 2. Password Hashing
- passlib with bcrypt scheme
- CryptContext configuration
- Hash password before storage
- Verify password hash on login

## 3. JWT Token Operations
- python-jose library
- Token encoding with user payload
- Token decoding and validation
- Token expiry handling
- Shared secret management

## 4. Database Operations with SQLModel
- User model creation
- Async session handling
- Query users by email
- Insert new users
- Handle unique constraints

## 5. Request/Response Models
- Pydantic BaseModel for validation
- UserCreate schema
- UserLogin schema
- TokenResponse schema
- Error response models

## 6. Environment Configuration
- python-dotenv for .env files
- Environment variable validation
- Secret key management
- Database URL handling

## 7. CORS and Security Headers
- FastAPI CORS middleware
- Allowed origins configuration
- Security headers setup

## 8. Error Handling
- HTTP status codes (401, 403, 422, 500)
- Custom error messages
- Exception handling
- Validation error formatting