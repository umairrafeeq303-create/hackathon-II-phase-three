# Feature Specification: Authentication & User Management System

**Feature Branch**: `001-auth`
**Created**: 2026-01-09
**Status**: Draft
**Input**: Authentication & User Management System for Phase II Todo Full-Stack Web Application

## Overview

This specification defines the authentication and user management system that provides secure user registration, login, and session management for the Todo Full-Stack Web Application. This is Spec 1 of 3 total specifications for Phase II.

**Purpose**: Enable users to create accounts, securely authenticate, and maintain sessions across the Next.js frontend and FastAPI backend using JWT tokens.

**Key Stakeholders**:
- End users (need secure account creation and login)
- Frontend application (Next.js with Better Auth)
- Backend API (FastAPI with JWT verification)
- Database (Neon PostgreSQL for user data storage)

**Success Criteria**:
- Users can create accounts and log in within 1 minute
- Authentication system supports 1000+ concurrent users
- Zero unauthorized access incidents (100% token validation)
- 95% of users successfully complete signup/signin on first attempt
- System maintains session security with 7-day token expiry

## User Scenarios & Testing *(mandatory)*

### User Story 1 - New User Registration (Priority: P1)

A new user wants to create an account to use the todo application. They provide their name, email address, and password. The system validates their information, creates a secure account, and logs them in immediately.

**Why this priority**: Account creation is the entry point to the application. Without user registration, no other features are accessible. This is the foundation of user data isolation.

**Independent Test**: Can be fully tested by submitting a registration form with valid credentials and verifying that a user record is created in the database and a JWT token is returned.

**Acceptance Scenarios**:

1. **Given** the user is on the signup page, **When** they enter a valid name, unique email, and password (minimum 8 characters), **Then** the system creates their account, returns a JWT token, and redirects them to the application
2. **Given** the user enters an email that already exists, **When** they submit the form, **Then** the system returns an error message "Email already registered" with 400 status code
3. **Given** the user enters a password with fewer than 8 characters, **When** they submit the form, **Then** the system returns an error message "Password must be at least 8 characters" with 422 status code
4. **Given** the user enters an invalid email format, **When** they submit the form, **Then** the system returns an error message "Invalid email format" with 422 status code

---

### User Story 2 - Returning User Login (Priority: P1)

A registered user returns to the application and wants to access their tasks. They provide their email and password. The system validates their credentials and provides access to their account.

**Why this priority**: Login is equally critical to registration. Users must be able to return to their accounts to access their data. This is also P1 because it's required for all subsequent features.

**Independent Test**: Can be fully tested by submitting login credentials for an existing user and verifying that a valid JWT token is returned and the user can access protected resources.

**Acceptance Scenarios**:

1. **Given** the user is on the signin page, **When** they enter their correct email and password, **Then** the system returns a JWT token and redirects them to their tasks dashboard
2. **Given** the user enters an incorrect password, **When** they submit the form, **Then** the system returns an error message "Invalid credentials" with 401 status code (no indication of which field is wrong for security)
3. **Given** the user enters an email that doesn't exist, **When** they submit the form, **Then** the system returns an error message "Invalid credentials" with 401 status code (consistent with wrong password for security)
4. **Given** the user enters empty email or password, **When** they submit the form, **Then** the system returns an error message "Email and password are required" with 400 status code

---

### User Story 3 - Authenticated Resource Access (Priority: P2)

A logged-in user wants to access protected resources (their todo tasks). The system validates their JWT token on every request to ensure they are authorized and extracts their user identity to enforce data isolation.

**Why this priority**: This story enables the integration between authentication and the rest of the application. It's P2 because it depends on P1 stories (users must be able to log in first) but is required before any task operations.

**Independent Test**: Can be fully tested by making API requests with valid and invalid JWT tokens and verifying that protected endpoints correctly accept/reject requests based on token validity.

**Acceptance Scenarios**:

1. **Given** the user has a valid JWT token, **When** they make a request to a protected endpoint with the token in the Authorization header, **Then** the system validates the token and processes the request
2. **Given** the user has no JWT token, **When** they make a request to a protected endpoint, **Then** the system returns an error "Authorization header required" with 401 status code
3. **Given** the user has an expired JWT token, **When** they make a request to a protected endpoint, **Then** the system returns an error "Token expired" with 401 status code
4. **Given** the user has an invalid/malformed JWT token, **When** they make a request to a protected endpoint, **Then** the system returns an error "Invalid token" with 401 status code
5. **Given** the user has a valid JWT token but tries to access another user's resources (user_id mismatch), **When** they make the request, **Then** the system returns an error "Forbidden" with 403 status code

---

### User Story 4 - User Session Management (Priority: P3)

A logged-in user wants to log out of the application. The system clears their session and requires re-authentication for subsequent requests.

**Why this priority**: Logout is important for security but is lower priority than core authentication flows. Users can still use the app without explicit logout (tokens expire automatically after 7 days).

**Independent Test**: Can be fully tested by logging in, logging out, and verifying that the JWT token is cleared from client storage and subsequent requests require re-authentication.

**Acceptance Scenarios**:

1. **Given** the user is logged in, **When** they click the logout button, **Then** the system clears their JWT token from client storage and redirects them to the signin page
2. **Given** the user has logged out, **When** they try to access a protected page, **Then** the system redirects them to the signin page

---

### User Story 5 - Retrieve Current User Information (Priority: P3)

A logged-in user's application wants to display their profile information (name, email). The system provides an endpoint to retrieve the authenticated user's data.

**Why this priority**: This is a convenience feature for UI personalization. It's P3 because the application can function without displaying user info, and the user_id is already available in the JWT token for core operations.

**Independent Test**: Can be fully tested by calling the /api/auth/me endpoint with a valid JWT token and verifying that the correct user information is returned.

**Acceptance Scenarios**:

1. **Given** the user is logged in with a valid JWT token, **When** they request their user information, **Then** the system returns their id, name, email, and created_at timestamp (excluding password)
2. **Given** the user's JWT token is invalid or expired, **When** they request their user information, **Then** the system returns an error with 401 status code

---

### Edge Cases

- What happens when a user tries to register with an email that's already taken?
  - System returns 400 Bad Request with message "Email already registered"
- What happens when a JWT token expires during an active session?
  - System returns 401 Unauthorized; frontend redirects to signin page
- What happens when the database connection fails during signup?
  - System returns 500 Internal Server Error with message "Service temporarily unavailable"
- What happens when the BETTER_AUTH_SECRET is missing or misconfigured?
  - Application fails to start with clear error message in logs (fail-fast approach)
- What happens when a user submits malformed JSON in request body?
  - System returns 422 Validation Error with details about which fields are invalid
- What happens when multiple concurrent signups attempt to use the same email?
  - Database unique constraint prevents duplicates; one succeeds, others receive 400 error
- What happens when a user's password contains special characters?
  - System accepts all printable characters; bcrypt handles special characters correctly

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow new users to register with name, email, and password
- **FR-002**: System MUST validate email addresses for correct format (RFC 5322 compliant)
- **FR-003**: System MUST enforce password minimum length of 8 characters
- **FR-004**: System MUST prevent duplicate email registration (email uniqueness)
- **FR-005**: System MUST hash passwords using bcrypt with minimum 10 salt rounds before storage
- **FR-006**: System MUST never store or log plain-text passwords
- **FR-007**: System MUST generate JWT tokens upon successful signup or signin
- **FR-008**: System MUST include user_id, email, exp (expiry), and iat (issued at) in JWT payload
- **FR-009**: System MUST sign JWT tokens using HS256 algorithm with BETTER_AUTH_SECRET
- **FR-010**: System MUST set JWT token expiry to 7 days from issuance
- **FR-011**: System MUST validate JWT tokens on all protected endpoint requests
- **FR-012**: System MUST extract Authorization header in format "Bearer <token>" from requests
- **FR-013**: System MUST verify JWT signature and expiry on every protected request
- **FR-014**: System MUST reject requests with missing, invalid, or expired JWT tokens with 401 status
- **FR-015**: System MUST extract user_id from validated JWT token for request processing
- **FR-016**: System MUST verify that user_id in JWT matches user_id in URL path for resource access
- **FR-017**: System MUST return 403 Forbidden when user_id mismatch is detected
- **FR-018**: System MUST allow users to authenticate with email and password
- **FR-019**: System MUST verify password against stored hash using bcrypt comparison
- **FR-020**: System MUST return consistent error message "Invalid credentials" for wrong email or password (prevent user enumeration)
- **FR-021**: System MUST provide endpoint to retrieve authenticated user's information (excluding password)
- **FR-022**: System MUST allow users to logout (frontend clears token)
- **FR-023**: System MUST store user records with id (UUID), email, name, hashed_password, and created_at
- **FR-024**: System MUST index email field for efficient lookup during signin
- **FR-025**: System MUST enforce unique constraint on email field at database level
- **FR-026**: System MUST return appropriate HTTP status codes: 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 403 (forbidden), 422 (validation error), 500 (server error)
- **FR-027**: System MUST never include hashed_password field in API responses
- **FR-028**: System MUST configure CORS to allow requests only from configured frontend origin
- **FR-029**: System MUST use PostgreSQL database via DATABASE_URL environment variable
- **FR-030**: System MUST share BETTER_AUTH_SECRET between frontend and backend for JWT operations

### Key Entities

- **User**: Represents an authenticated user of the todo application
  - Unique identifier (UUID)
  - Email address (unique, used for authentication)
  - Display name (for UI personalization)
  - Securely hashed password (bcrypt)
  - Account creation timestamp
  - Relationships: One user has many tasks (defined in Spec 2)

- **JWT Token**: Represents an authenticated session (not stored in database)
  - User identifier (links token to user)
  - User email (for UI context)
  - Issued at timestamp (when token was created)
  - Expiration timestamp (when token becomes invalid)
  - Signature (cryptographic proof of authenticity)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete account registration in under 60 seconds
- **SC-002**: Users can complete signin in under 30 seconds
- **SC-003**: System handles 1000 concurrent authentication requests without degradation
- **SC-004**: JWT token validation adds less than 50ms latency to protected requests
- **SC-005**: 100% of protected endpoints validate JWT tokens (zero unauthorized access)
- **SC-006**: 95% of signup attempts succeed on first try for valid inputs
- **SC-007**: 98% of signin attempts succeed on first try for correct credentials
- **SC-008**: Zero plain-text passwords stored in database or logs (100% hashing compliance)
- **SC-009**: Password verification time is consistent (300-500ms) regardless of correctness (timing attack prevention)
- **SC-010**: System maintains 99.9% authentication service uptime
- **SC-011**: All API endpoints return appropriate HTTP status codes (100% compliance)
- **SC-012**: JWT tokens expire exactly 7 days after issuance (no grace period)

### Assumptions

- Users have access to a valid email address
- Users can remember or store their passwords securely
- Frontend application will store JWT tokens securely (localStorage or sessionStorage with appropriate security considerations)
- Network connection is stable enough for authentication requests
- Database (Neon PostgreSQL) is available and responsive
- BETTER_AUTH_SECRET is generated as a strong random string (minimum 32 characters)
- Frontend and backend share the same BETTER_AUTH_SECRET value exactly
- System clock synchronization is accurate for JWT expiry validation
- HTTPS will be enforced in production deployment (specified in Deployment spec)

## Database Schema

### User Table (SQLModel)

**Table Name**: `users`

**Fields**:
- `id`: String (UUID) - Primary Key - Auto-generated UUID v4
- `email`: String - Unique, Not Null, Indexed - Maximum 255 characters
- `name`: String - Not Null - Maximum 100 characters - User's display name
- `hashed_password`: String - Not Null - Bcrypt hash output (60 characters)
- `created_at`: DateTime - Not Null - Default: current timestamp - UTC timezone

**Indexes**:
- Primary: `id` (automatic)
- Unique: `email` (for preventing duplicates and efficient signin lookup)

**Constraints**:
- `email` must be unique across all records
- `email` must not be null or empty
- `name` must not be null or empty
- `hashed_password` must not be null
- `created_at` must not be null

**Example SQLModel Definition** (conceptual, not implementation):
```python
# This is for specification purposes only - actual implementation in planning phase
class User(SQLModel, table=True):
    id: UUID (primary key, default=uuid4)
    email: str (unique, indexed, max_length=255)
    name: str (max_length=100)
    hashed_password: str (max_length=60)
    created_at: datetime (default=utcnow)
```

**SQL Schema** (for reference):
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

## API Specification

### Endpoint 1: User Signup

**Method and Path**: `POST /api/auth/signup`

**Authentication Required**: No

**Request Schema**:
```json
{
  "name": "string (required, 1-100 characters)",
  "email": "string (required, valid email format, max 255 characters)",
  "password": "string (required, minimum 8 characters)"
}
```

**Request Example**:
```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "created_at": "2026-01-09T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

*400 Bad Request - Email Already Exists*:
```json
{
  "detail": "Email already registered"
}
```

*422 Validation Error - Invalid Input*:
```json
{
  "detail": [
    {
      "loc": ["body", "password"],
      "msg": "Password must be at least 8 characters",
      "type": "value_error"
    }
  ]
}
```

*422 Validation Error - Invalid Email*:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "Invalid email format",
      "type": "value_error"
    }
  ]
}
```

*500 Internal Server Error*:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Status Codes**:
- 201: User created successfully, token returned
- 400: Email already registered
- 422: Validation failed (invalid email, short password, missing fields)
- 500: Server error (database unavailable, configuration error)

---

### Endpoint 2: User Signin

**Method and Path**: `POST /api/auth/signin`

**Authentication Required**: No

**Request Schema**:
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required)"
}
```

**Request Example**:
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "created_at": "2026-01-09T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

*401 Unauthorized - Invalid Credentials*:
```json
{
  "detail": "Invalid credentials"
}
```

*400 Bad Request - Missing Fields*:
```json
{
  "detail": "Email and password are required"
}
```

*500 Internal Server Error*:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Status Codes**:
- 200: Authentication successful, token returned
- 400: Missing required fields
- 401: Invalid email or password (same message for both to prevent user enumeration)
- 500: Server error

---

### Endpoint 3: Get Current User

**Method and Path**: `GET /api/auth/me`

**Authentication Required**: Yes (JWT token in Authorization header)

**Request Headers**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "created_at": "2026-01-09T10:30:00Z"
}
```

**Error Responses**:

*401 Unauthorized - Missing Token*:
```json
{
  "detail": "Authorization header required"
}
```

*401 Unauthorized - Invalid Token*:
```json
{
  "detail": "Invalid token"
}
```

*401 Unauthorized - Expired Token*:
```json
{
  "detail": "Token expired"
}
```

*500 Internal Server Error*:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Status Codes**:
- 200: User information returned successfully
- 401: Missing, invalid, or expired token
- 500: Server error

---

### JWT Token Structure

**Algorithm**: HS256 (HMAC with SHA-256)

**Secret**: Value of BETTER_AUTH_SECRET environment variable (shared between frontend and backend)

**Token Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "exp": 1736500200,
  "iat": 1735895400
}
```

**Payload Fields**:
- `user_id`: String (UUID) - Unique identifier for the user
- `email`: String - User's email address (for UI context)
- `exp`: Integer - Expiration timestamp (Unix epoch, 7 days from iat)
- `iat`: Integer - Issued at timestamp (Unix epoch, current time)

**Token Format**: Three base64-encoded parts separated by dots
```
<header>.<payload>.<signature>
```

**Example Token**:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTczNjUwMDIwMCwiaWF0IjoxNzM1ODk1NDAwfQ.signature_here
```

**Token Transmission**:
- Frontend: Includes token in `Authorization` header for all protected requests
- Format: `Authorization: Bearer <token>`
- Storage: Frontend stores token in localStorage or sessionStorage (implementation detail in Spec 3)

**Token Expiry**:
- Duration: 7 days (604800 seconds) from issuance
- No refresh token strategy in this version (users must re-authenticate after expiry)
- Expired tokens are rejected with 401 status code

## Frontend Integration Requirements

### Better Auth Setup

**Installation**:
- Better Auth must be installed as npm dependency in Next.js frontend
- JWT plugin for Better Auth must be configured

**Configuration Location**:
- Better Auth configuration in `lib/auth.ts` or similar (exact path determined in Spec 3)
- Environment variables in `.env.local` for frontend

**Required Configuration**:
```typescript
// Conceptual configuration - not implementation code
{
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL
  },
  plugins: {
    jwt: {
      secret: process.env.BETTER_AUTH_SECRET,
      expiresIn: "7d"
    }
  },
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL
  }
}
```

**API Routes**:
- Better Auth exposes routes under `/api/auth/[...all]` catch-all route in Next.js
- These routes handle Better Auth's internal operations
- Custom auth endpoints (signup, signin, me) are separate FastAPI backend endpoints

### JWT Token Storage

**Storage Location**: localStorage (primary) or sessionStorage (alternative)

**Storage Key**: `auth_token` or similar constant

**Storage Operations**:
- Set token: Store JWT string after successful signup/signin
- Get token: Retrieve JWT string for Authorization header
- Remove token: Delete JWT string on logout

**Security Considerations**:
- localStorage persists across browser sessions (user stays logged in)
- sessionStorage clears when tab closes (more secure, less convenient)
- Both are vulnerable to XSS attacks (mitigated by Next.js built-in XSS protection)
- HTTPS required in production to prevent token interception

### API Client Configuration

**Base URL**: Value from `NEXT_PUBLIC_API_URL` environment variable (points to FastAPI backend)

**Request Interceptor** (conceptual):
- Automatically add Authorization header to all requests to protected endpoints
- Format: `Authorization: Bearer ${token}`
- Handle 401 responses by redirecting to signin page

**Error Handling**:
- 401 errors: Clear token, redirect to signin page
- Network errors: Display user-friendly error message
- 500 errors: Display "Service temporarily unavailable" message

### Session Management

**Login Flow**:
1. User submits credentials via signin form
2. Frontend calls POST /api/auth/signin
3. Backend validates credentials and returns JWT token
4. Frontend stores token in localStorage
5. Frontend redirects user to dashboard

**Protected Page Access**:
1. Frontend checks for token in localStorage
2. If no token: Redirect to signin page
3. If token exists: Include in Authorization header for API calls
4. If API returns 401: Clear token, redirect to signin page

**Logout Flow**:
1. User clicks logout button
2. Frontend removes token from localStorage
3. Frontend redirects to signin page
4. Subsequent requests lack Authorization header (fail with 401)

**Token Expiry Handling**:
- Frontend does not validate token expiry (delegated to backend)
- When backend returns 401 for expired token, frontend clears token and redirects
- No automatic token refresh mechanism (users re-authenticate after 7 days)

## Backend Implementation Requirements

### FastAPI Application Structure

**File Organization**:
- User model: SQLModel definition for users table
- Auth routes: Endpoints for signup, signin, me
- Auth utilities: Password hashing, JWT generation/verification
- Database: Connection management and session handling
- Middleware/Dependencies: JWT verification for protected routes

**Configuration**:
- Environment variables loaded at startup
- Database connection established at startup
- CORS middleware configured with frontend origin
- FastAPI automatic Swagger UI documentation at /docs

### Authentication Middleware/Dependency

**JWT Verification Dependency** (conceptual):
```python
# Conceptual flow - not implementation code
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Extract token from Authorization header
    # Verify token signature using BETTER_AUTH_SECRET
    # Check token expiry
    # Extract user_id from payload
    # Return user_id for use in route handlers
    # Raise 401 error if verification fails
```

**Usage Pattern**:
- Protected routes declare dependency: `current_user: str = Depends(get_current_user)`
- Dependency automatically extracts and validates JWT token
- Route handler receives verified user_id as parameter
- No manual token handling in route logic

**Error Handling**:
- Missing token: Raise 401 with "Authorization header required"
- Invalid signature: Raise 401 with "Invalid token"
- Expired token: Raise 401 with "Token expired"
- Malformed token: Raise 401 with "Invalid token"

### Password Hashing Utilities

**Hashing Function** (conceptual):
```python
# Conceptual flow - not implementation code
def hash_password(password: str) -> str:
    # Use bcrypt with 10 salt rounds minimum
    # Return hashed password string (60 characters)
```

**Verification Function** (conceptual):
```python
# Conceptual flow - not implementation code
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Use bcrypt to compare plain password with hash
    # Return True if match, False otherwise
    # Execution time should be consistent to prevent timing attacks
```

**Requirements**:
- Use passlib library with bcrypt backend
- Salt rounds: 10 (configurable via environment variable if needed)
- Never log or store plain-text passwords
- Consistent execution time for verification (timing attack prevention)

### JWT Utilities

**Token Generation Function** (conceptual):
```python
# Conceptual flow - not implementation code
def create_access_token(user_id: str, email: str) -> str:
    # Create payload with user_id, email, iat, exp
    # exp = current_time + 7 days
    # iat = current_time
    # Sign with HS256 algorithm using BETTER_AUTH_SECRET
    # Return JWT token string
```

**Token Verification Function** (conceptual):
```python
# Conceptual flow - not implementation code
def verify_token(token: str) -> dict:
    # Decode token using BETTER_AUTH_SECRET
    # Verify signature with HS256
    # Check expiry (current_time < exp)
    # Return payload dict with user_id and email
    # Raise exception if verification fails
```

**Requirements**:
- Use python-jose library for JWT operations
- Algorithm: HS256 (specified in constants)
- Secret: BETTER_AUTH_SECRET from environment
- Token expiry: 7 days (604800 seconds)
- Validate both signature and expiry on every verification

### Database Session Management

**Connection Pooling**:
- SQLModel/SQLAlchemy manages connection pool automatically
- Database URL from DATABASE_URL environment variable
- Pool size and timeout configured for production load

**Session Per Request**:
- Each API request gets its own database session
- Session is committed on successful response
- Session is rolled back on error
- Session is always closed after request (in finally block)

**Dependency Pattern** (conceptual):
```python
# Conceptual flow - not implementation code
async def get_db_session():
    # Create session
    # Yield session to route handler
    # Commit session on success
    # Rollback on exception
    # Always close session
```

**Error Handling**:
- Database connection errors: Return 500 with generic message
- Unique constraint violations: Return 400 with specific message (e.g., "Email already registered")
- Other database errors: Return 500 with generic message (don't leak schema details)

## Security Considerations

### Threat Model

**Threats Addressed**:
1. **Unauthorized Access**: JWT token validation prevents access without authentication
2. **Password Theft**: Bcrypt hashing protects passwords even if database is compromised
3. **User Enumeration**: Consistent error messages prevent discovering which emails are registered
4. **Token Theft**: HTTPS in production prevents man-in-the-middle attacks
5. **Cross-Site Request Forgery (CSRF)**: JWT tokens in Authorization header (not cookies) resist CSRF
6. **SQL Injection**: SQLModel ORM parameterization prevents SQL injection
7. **Timing Attacks**: Consistent password verification time prevents timing-based user enumeration

**Threats Not Addressed** (Out of Scope):
- XSS attacks (mitigated by Next.js framework defaults, not auth system responsibility)
- Brute force attacks (rate limiting not included in this spec)
- Session fixation (not applicable with stateless JWT tokens)
- Password reset vulnerabilities (password reset not in scope)

### Mitigation Strategies

**Password Security**:
- Minimum 8 character requirement enforced at API level
- Bcrypt hashing with 10 salt rounds minimum
- Never log or store plain-text passwords
- Password hashes never included in API responses

**Token Security**:
- JWT tokens signed with strong secret (BETTER_AUTH_SECRET, minimum 32 characters recommended)
- Tokens expire after 7 days (limited blast radius if stolen)
- Token signature verified on every protected request
- Tokens transmitted in Authorization header (not URL or cookie without httpOnly flag)

**User Enumeration Prevention**:
- Signin returns "Invalid credentials" for both wrong email and wrong password
- Password verification time is consistent regardless of correctness
- Signup returns generic error for duplicate email (no confirmation that email exists)

**Database Security**:
- SQLModel ORM prevents SQL injection through parameterized queries
- Unique constraint on email prevents race conditions in duplicate registration
- Database credentials in environment variables (not hardcoded)

**CORS Protection**:
- Backend configured to accept requests only from frontend origin
- Credentials (cookies, authorization headers) allowed only for configured origin
- Prevents unauthorized websites from calling API

**HTTPS Enforcement**:
- Production deployment must use HTTPS for all communication
- Prevents token interception via man-in-the-middle attacks
- Environment variable or deployment configuration enforces HTTPS

### Security Best Practices Checklist

- [ ] Passwords hashed with bcrypt (10+ salt rounds)
- [ ] JWT tokens signed with strong secret (32+ characters)
- [ ] JWT tokens expire after 7 days maximum
- [ ] All protected endpoints validate JWT tokens
- [ ] User_id in token matches user_id in URL path
- [ ] Password hashes never returned in API responses
- [ ] Plain-text passwords never logged or stored
- [ ] Consistent error messages prevent user enumeration
- [ ] CORS configured to allow only frontend origin
- [ ] HTTPS enforced in production deployment
- [ ] Database credentials in environment variables
- [ ] SQL injection prevented via ORM parameterization
- [ ] Email uniqueness enforced at database level
- [ ] Token verification includes both signature and expiry checks
- [ ] Authorization header format validated (Bearer <token>)

## Testing Strategy

### Unit Tests (Backend)

**Password Hashing**:
- Test password is hashed correctly (output is bcrypt format)
- Test hashed password can be verified with correct plain password
- Test hashed password fails verification with incorrect plain password
- Test hashing same password twice produces different hashes (salt is random)

**JWT Token Generation**:
- Test token contains correct payload (user_id, email, exp, iat)
- Test token expiry is exactly 7 days from issuance
- Test token can be decoded with correct secret
- Test token cannot be decoded with wrong secret

**JWT Token Verification**:
- Test valid token is verified successfully
- Test expired token is rejected
- Test token with invalid signature is rejected
- Test token with missing claims is rejected

**User Model**:
- Test user can be created with valid data
- Test email uniqueness constraint is enforced
- Test created_at timestamp is set automatically

### Integration Tests

**Signup Flow**:
- Test new user can register with valid credentials
- Test registration returns JWT token
- Test duplicate email registration is rejected
- Test password shorter than 8 characters is rejected
- Test invalid email format is rejected

**Signin Flow**:
- Test user can signin with correct credentials
- Test signin returns JWT token
- Test wrong password is rejected with "Invalid credentials"
- Test non-existent email is rejected with "Invalid credentials"
- Test returned token is valid and can access protected endpoints

**Protected Endpoint Access**:
- Test request with valid JWT token succeeds
- Test request without token is rejected with 401
- Test request with expired token is rejected with 401
- Test request with invalid token is rejected with 401
- Test request with user_id mismatch is rejected with 403

**Get Current User**:
- Test returns correct user data for authenticated request
- Test excludes hashed_password from response
- Test rejects unauthenticated request with 401

### Manual Testing Checklist

- [ ] User can complete signup flow from frontend form to successful login
- [ ] Duplicate email registration shows appropriate error message
- [ ] Short password shows validation error before submitting
- [ ] User can signin with registered credentials
- [ ] Wrong password shows "Invalid credentials" error
- [ ] Non-existent email shows "Invalid credentials" error
- [ ] Authenticated user can access protected pages
- [ ] Unauthenticated user is redirected to signin page when accessing protected pages
- [ ] User can logout and is redirected to signin page
- [ ] Token expires after 7 days (can be tested with manual token manipulation)
- [ ] CORS allows frontend requests and blocks unauthorized origins
- [ ] API documentation (Swagger UI) at /docs is accessible and accurate
- [ ] Database contains user record with hashed password (not plain-text)
- [ ] JWT token payload contains correct user_id and email

## Integration Points with Other Specs

### Spec 2: Task CRUD API

**Provides to Spec 2**:
- JWT token format and validation mechanism (Spec 2 uses same verification dependency)
- User_id extraction from JWT tokens (Spec 2 uses user_id for task ownership filtering)
- User table schema (Spec 2 references users.id as foreign key for tasks.user_id)
- Authentication dependency pattern (Spec 2 applies to all task endpoints)

**Requirements for Spec 2**:
- Spec 2 must use the same JWT verification dependency for all task endpoints
- Spec 2 must extract user_id from authenticated requests for data isolation
- Spec 2 must validate that task.user_id matches authenticated user_id before mutations
- Spec 2 must return 403 Forbidden if user tries to access another user's tasks

### Spec 3: Frontend UI Components

**Provides to Spec 3**:
- JWT token (stored by Spec 3 in localStorage/sessionStorage)
- Authentication state (Spec 3 checks token presence for UI rendering)
- User information from /api/auth/me (Spec 3 displays in UI header/profile)
- Signup/signin API contracts (Spec 3 implements forms to match schemas)

**Requirements for Spec 3**:
- Spec 3 must implement signup and signin forms matching API request schemas
- Spec 3 must store JWT token in browser storage after successful authentication
- Spec 3 must include JWT token in Authorization header for all task API requests
- Spec 3 must redirect to signin page when token is missing or API returns 401
- Spec 3 must implement logout by clearing stored token
- Spec 3 must not attempt to validate JWT token client-side (delegate to backend)

### Shared Database Connection

**Database**: Neon PostgreSQL
**Connection**: Both specs use DATABASE_URL environment variable
**Shared Secret**: Both specs use BETTER_AUTH_SECRET environment variable
**Isolation**: Specs operate on different tables (users vs tasks) but share connection pool

## Environment Variables

### Backend (FastAPI)

- **DATABASE_URL**: Neon PostgreSQL connection string
  - Format: `postgresql://user:password@host:port/database?sslmode=require`
  - Required: Yes
  - Example: `postgresql://user:pass@ep-xyz-123.us-east-2.aws.neon.tech/todo_db?sslmode=require`

- **BETTER_AUTH_SECRET**: Shared secret for JWT signing/verification
  - Format: Strong random string, minimum 32 characters
  - Required: Yes
  - Example: `your-super-secret-jwt-key-min-32-chars-long-random-string`
  - Must match frontend value exactly

- **ALGORITHM**: JWT signing algorithm
  - Format: String
  - Required: No (default: "HS256")
  - Value: `HS256`

- **ACCESS_TOKEN_EXPIRE_DAYS**: JWT token expiry duration
  - Format: Integer (days)
  - Required: No (default: 7)
  - Value: `7`

- **FRONTEND_URL**: Frontend origin for CORS configuration
  - Format: URL string
  - Required: Yes
  - Example: `http://localhost:3000` (development) or `https://todo-app.vercel.app` (production)

### Frontend (Next.js)

- **NEXT_PUBLIC_API_URL**: Backend API base URL
  - Format: URL string
  - Required: Yes
  - Example: `http://localhost:8000` (development) or `https://todo-api.railway.app` (production)
  - Must be NEXT_PUBLIC_ prefix for client-side access

- **BETTER_AUTH_SECRET**: Shared secret for JWT operations (Better Auth configuration)
  - Format: Strong random string, minimum 32 characters
  - Required: Yes
  - Example: `your-super-secret-jwt-key-min-32-chars-long-random-string`
  - Must match backend value exactly

- **DATABASE_URL**: Neon PostgreSQL connection string (for Better Auth database adapter)
  - Format: Same as backend DATABASE_URL
  - Required: Yes (if Better Auth directly accesses database; may be optional if all auth operations go through backend)
  - Example: Same as backend DATABASE_URL

### Environment Variable Template Files

**Backend `.env.example`**:
```
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
BETTER_AUTH_SECRET=your-super-secret-jwt-key-min-32-chars-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=7
FRONTEND_URL=http://localhost:3000
```

**Frontend `.env.local.example`**:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-super-secret-jwt-key-min-32-chars-long-random-string
DATABASE_URL=postgresql://user:password@host:port/database?sslmode=require
```

**Critical Requirements**:
- BETTER_AUTH_SECRET must be identical in both frontend and backend
- DATABASE_URL must point to the same Neon PostgreSQL instance
- FRONTEND_URL in backend must match the actual frontend deployment URL
- NEXT_PUBLIC_API_URL must match the actual backend deployment URL

## Acceptance Criteria

### User Registration

- [ ] User can signup with valid name, email, and password (8+ characters)
- [ ] User cannot signup with duplicate email (returns 400 with "Email already registered")
- [ ] User cannot signup with password shorter than 8 characters (returns 422 validation error)
- [ ] User cannot signup with invalid email format (returns 422 validation error)
- [ ] Successful signup returns JWT token and user object (without password)
- [ ] Password is hashed with bcrypt (10+ salt rounds) before database storage
- [ ] Plain-text password is never logged or stored
- [ ] User record in database has id (UUID), email, name, hashed_password, created_at

### User Authentication

- [ ] User can signin with correct email and password
- [ ] Successful signin returns JWT token and user object (without password)
- [ ] User cannot signin with wrong password (returns 401 with "Invalid credentials")
- [ ] User cannot signin with non-existent email (returns 401 with "Invalid credentials")
- [ ] Error message is identical for wrong password and non-existent email (prevents user enumeration)
- [ ] Signin validation time is consistent (300-500ms) regardless of correctness

### JWT Token Management

- [ ] JWT token is generated on successful signup and signin
- [ ] JWT token payload contains user_id, email, exp, iat
- [ ] JWT token is signed with HS256 algorithm using BETTER_AUTH_SECRET
- [ ] JWT token expires exactly 7 days after issuance
- [ ] JWT token can be verified with correct secret
- [ ] Invalid JWT token is rejected with 401 status code
- [ ] Expired JWT token is rejected with 401 status code
- [ ] JWT token signature mismatch is rejected with 401 status code

### Protected Endpoint Access

- [ ] Request with valid JWT token in Authorization header is accepted
- [ ] Request without Authorization header is rejected with 401
- [ ] Request with "Authorization: Bearer <invalid_token>" is rejected with 401
- [ ] Request with "Authorization: Bearer <expired_token>" is rejected with 401
- [ ] Protected endpoint extracts user_id from validated JWT token
- [ ] Request with user_id mismatch (token user_id != URL user_id) is rejected with 403

### Get Current User Endpoint

- [ ] GET /api/auth/me with valid token returns user object
- [ ] Returned user object contains id, email, name, created_at
- [ ] Returned user object excludes hashed_password field
- [ ] GET /api/auth/me without token is rejected with 401
- [ ] GET /api/auth/me with invalid/expired token is rejected with 401

### User Data Isolation

- [ ] Users can only access their own data (verified by user_id in JWT)
- [ ] Attempt to access another user's resources returns 403 Forbidden
- [ ] User_id from JWT token is used for all database queries
- [ ] User_id in JWT matches user_id in URL path for protected resources

### Database Schema

- [ ] Users table exists with correct schema (id, email, name, hashed_password, created_at)
- [ ] Email field has unique constraint at database level
- [ ] Email field is indexed for efficient lookup
- [ ] User id is UUID format, not sequential integer
- [ ] Passwords are stored as bcrypt hashes (60 characters)
- [ ] Created_at timestamp is set automatically to current UTC time

### Security Compliance

- [ ] CORS is configured to allow only frontend origin
- [ ] HTTPS is enforced in production deployment
- [ ] BETTER_AUTH_SECRET is stored in environment variables (not hardcoded)
- [ ] DATABASE_URL is stored in environment variables (not hardcoded)
- [ ] Password hashes never appear in API responses
- [ ] Plain-text passwords never appear in logs
- [ ] JWT secret is minimum 32 characters and cryptographically random
- [ ] All API endpoints return appropriate HTTP status codes (200, 201, 400, 401, 403, 422, 500)

### Integration with Other Specs

- [ ] JWT token format is compatible with Spec 2 (Task API) verification
- [ ] User_id extracted from JWT can be used by Spec 2 for task ownership
- [ ] User table schema supports foreign key from tasks.user_id
- [ ] Authentication dependency can be reused by Spec 2 endpoints
- [ ] Frontend (Spec 3) can store JWT token and include in API requests
- [ ] API response schemas match what Frontend (Spec 3) expects

### Error Handling

- [ ] All error responses are JSON format with "detail" field
- [ ] Error messages are user-friendly and don't leak technical details
- [ ] Database errors return 500 with generic message (don't expose schema)
- [ ] Validation errors return 422 with specific field information
- [ ] Authorization errors return 401 or 403 with appropriate message
- [ ] Server errors return 500 with "Service temporarily unavailable"

---

## Notes

This specification focuses on WHAT the authentication system must do and WHY each requirement exists, without prescribing HOW to implement it. Implementation details (specific libraries, code structure, file organization) will be determined in the planning phase (`/sp.plan`).

The specification is complete and ready for planning. No clarifications are needed as all critical decisions have been documented with reasonable defaults based on industry standards and the project constitution.
