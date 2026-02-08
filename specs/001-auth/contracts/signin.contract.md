# Contract: User Signin Endpoint

**Endpoint**: `POST /api/auth/signin`
**Version**: v1.0
**Authentication**: Not required
**Purpose**: Authenticate existing user and return JWT token

## Request

### HTTP Method
```
POST
```

### URL Path
```
/api/auth/signin
```

### Headers
```
Content-Type: application/json
```

### Request Body Schema

```typescript
{
  email: string;     // Required, user's registered email address
  password: string;  // Required, user's password
}
```

### Request Body Constraints

| Field | Type | Required | Constraints | Validation |
|-------|------|----------|-------------|------------|
| `email` | string | Yes | Valid email format, max 255 characters | RFC 5322 format, case-insensitive |
| `password` | string | Yes | Any length (no minimum check at signin) | Accept as provided |

**Note**: Password length is NOT validated at signin (only at signup). This prevents information leakage about password requirements.

### Request Example

```json
{
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

## Response

### Success Response (200 OK)

**Status Code**: `200 OK`

**Response Body Schema**:
```typescript
{
  user: {
    id: string;         // UUID v4 format
    email: string;      // User's email (lowercase)
    name: string;       // User's display name
    created_at: string; // ISO 8601 datetime (UTC)
  };
  token: string;        // JWT access token (valid for 7 days)
}
```

**Response Example**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john.doe@example.com",
    "name": "John Doe",
    "created_at": "2026-01-09T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTczNjUwMDIwMCwiaWF0IjoxNzM1ODk1NDAwfQ.signature_here"
}
```

**Response Headers**:
```
Content-Type: application/json
```

**Post-Success Actions**:
1. Frontend stores JWT token in localStorage
2. Frontend redirects user to dashboard/tasks page
3. Subsequent requests include token in Authorization header

---

## Error Responses

### Error 1: Invalid Credentials (401 Unauthorized)

**Condition**: Email not found OR password does not match

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Invalid credentials"
}
```

**Security Note**: Same error message for both "email not found" and "wrong password" to prevent user enumeration.

**Frontend Handling**:
- Display error message: "Invalid email or password. Please try again."
- Clear password field (keep email)
- Highlight both email and password fields
- Provide link to password reset (if implemented)
- Do NOT indicate which field is incorrect

---

### Error 2: Missing Required Fields (400 Bad Request)

**Condition**: Email or password field is missing from request

**Status Code**: `400 Bad Request`

**Response Body**:
```json
{
  "detail": "Email and password are required"
}
```

**Frontend Handling**:
- Display error message: "Please enter both email and password."
- Highlight empty fields
- This should be prevented by frontend validation

---

### Error 3: Empty Email or Password (400 Bad Request)

**Condition**: Email or password is empty string or whitespace-only

**Status Code**: `400 Bad Request`

**Response Body**:
```json
{
  "detail": "Email and password are required"
}
```

**Frontend Handling**:
- Same as Error 2
- Frontend should trim inputs and validate before submission

---

### Error 4: Invalid Email Format (422 Validation Error)

**Condition**: Email does not match RFC 5322 format

**Status Code**: `422 Unprocessable Entity`

**Response Body**:
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

**Frontend Handling**:
- Display error message: "Please enter a valid email address."
- Highlight email field
- This should be caught by frontend validation

---

### Error 5: Database Connection Failed (500 Internal Server Error)

**Condition**: Backend cannot connect to database

**Status Code**: `500 Internal Server Error`

**Response Body**:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Frontend Handling**:
- Display error message: "Service temporarily unavailable. Please try again in a few moments."
- Log error for monitoring
- Provide retry button
- Do NOT expose internal error details

---

### Error 6: Configuration Error (500 Internal Server Error)

**Condition**: BETTER_AUTH_SECRET is missing or JWT generation fails

**Status Code**: `500 Internal Server Error`

**Response Body**:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Frontend Handling**:
- Same as Error 5 (generic server error handling)
- Do NOT expose configuration details to user

---

## Security Considerations

### User Enumeration Prevention

1. **Consistent Error Message**: "Invalid credentials" for both wrong email and wrong password
2. **Consistent Response Time**: Password verification time MUST be consistent (300-500ms) regardless of whether email exists
   - If email not found: Still run bcrypt comparison with dummy hash
   - If email found: Run bcrypt comparison with actual hash
   - Both paths take same time

### Brute Force Protection

**Not implemented in this spec** (out of scope), but production should:
- Rate limiting: Max 5 failed attempts per IP per 15 minutes
- Account lockout: Temporary lockout after 10 failed attempts
- CAPTCHA: Required after 3 failed attempts
- Monitoring: Alert on suspicious patterns

### Password Handling

1. **Never Log Passwords**: Backend MUST NOT log the password field from requests
2. **Timing Attack Prevention**: Use bcrypt's built-in constant-time comparison
3. **No Password in Response**: Password never included in response

### Email Handling

1. **Case-Insensitive Lookup**: Email normalized to lowercase before database query
2. **Exact Match Required**: No partial email matching

## Authentication Flow

### Successful Login Flow
```
1. User submits email and password
2. Frontend validates email format (client-side)
3. Frontend sends POST request to /api/auth/signin
4. Backend normalizes email to lowercase
5. Backend queries database for user with email
6. Backend compares password with stored hash using bcrypt
7. Backend generates JWT token with user_id and email
8. Backend returns user info and token (200 OK)
9. Frontend stores token in localStorage
10. Frontend redirects to dashboard
```

### Failed Login Flow (Wrong Password)
```
1. User submits email and correct-format password
2. Frontend sends POST request to /api/auth/signin
3. Backend finds user by email
4. Backend compares password with hash → mismatch
5. Backend waits to match timing of successful verification
6. Backend returns "Invalid credentials" (401 Unauthorized)
7. Frontend displays error message
8. Frontend clears password field
```

### Failed Login Flow (Email Not Found)
```
1. User submits email that doesn't exist
2. Frontend sends POST request to /api/auth/signin
3. Backend queries database → no user found
4. Backend runs bcrypt comparison with dummy hash (timing attack prevention)
5. Backend waits to match timing of successful verification
6. Backend returns "Invalid credentials" (401 Unauthorized)
7. Frontend displays same error message as wrong password
```

## Testing

### Valid Request Test Cases

1. **Happy Path**: Correct email and password → 200 response with user and token
2. **Case-Insensitive Email**: Email with uppercase letters → 200 response
3. **Special Characters in Password**: Password with symbols → 200 response

### Invalid Request Test Cases

1. **Wrong Password**: Correct email, wrong password → 401 error "Invalid credentials"
2. **Non-Existent Email**: Email not in database → 401 error "Invalid credentials"
3. **Empty Email**: "" → 400 error "Email and password are required"
4. **Empty Password**: "" → 400 error "Email and password are required"
5. **Missing Email Field**: No email in request body → 400 error
6. **Missing Password Field**: No password in request body → 400 error
7. **Invalid Email Format**: "notanemail" → 422 error

### Security Test Cases

1. **Timing Attack Prevention**: Measure response time for:
   - Valid email, wrong password (should be ~300-500ms)
   - Non-existent email, any password (should be ~300-500ms)
   - Valid email, correct password (should be ~300-500ms)
   - All three should have similar response times

2. **Error Message Consistency**:
   - Wrong password → "Invalid credentials"
   - Non-existent email → "Invalid credentials"
   - Same message for both cases

### Error Handling Test Cases

1. **Database Down**: Simulate DB connection failure → 500 error
2. **JWT Generation Failure**: Simulate missing BETTER_AUTH_SECRET → 500 error

## Backend Implementation Notes

### Route Handler Signature
```python
@router.post("/signin", status_code=200, response_model=AuthResponse)
async def signin(
    user_login: UserLogin,
    db: Session = Depends(get_db_session)
) -> AuthResponse:
    # Implementation
```

### Implementation Steps
1. Validate request body (automatic via Pydantic)
2. Normalize email to lowercase
3. Query database for user by email
4. If user not found:
   - Run bcrypt comparison with dummy hash (timing attack prevention)
   - Wait to match successful verification time
   - Raise 401 error "Invalid credentials"
5. If user found:
   - Compare password with stored hash using bcrypt
   - If mismatch: Raise 401 error "Invalid credentials"
   - If match: Generate JWT token
6. Return user information and token

### Timing Attack Prevention Implementation
```python
# Conceptual implementation - not production code
async def signin(user_login: UserLogin, db: Session):
    user = db.query(User).filter(User.email == user_login.email.lower()).first()

    if not user:
        # Run dummy verification to match timing
        verify_password(user_login.password, "$2b$10$dummy_hash_for_timing")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Real verification
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate token and return
    token = create_access_token(user.id, user.email)
    return AuthResponse(user=user, token=token)
```

### Error Handling
- User not found → 401 with "Invalid credentials"
- Password mismatch → 401 with "Invalid credentials"
- Missing fields → 400 with "Email and password are required"
- `ValidationError` (Pydantic) → 422 with field-specific errors
- `Exception` (database/config errors) → 500 with generic message

## Frontend Implementation Notes

### API Client Function
```typescript
async function signin(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new SigninError(response.status, error.detail);
  }

  return response.json();
}
```

### Form Validation (Client-Side)
- Email format validation (before API call)
- Empty field validation
- Trim whitespace from email

### Success Handling
1. Store token in localStorage: `localStorage.setItem('auth_token', token)`
2. Update authentication state in React context/store
3. Redirect to `/dashboard` or `/tasks` page
4. Display welcome back message

### Error Handling
- 401 errors: Display "Invalid email or password" message
- 400 errors: Display "Please fill in all fields" message
- 422 errors: Display validation error (should be prevented by client-side validation)
- 500 errors: Display "Service unavailable" message with retry option
- Network errors: Display connection error message

### UX Considerations
- Keep email populated after failed attempt
- Clear password after failed attempt
- Show "Forgot password?" link (if implemented)
- Provide link to signup page for new users
- Consider adding "Remember me" option (extends token expiry)

## Contract Compliance Checklist

- [x] Request schema defined with all fields and constraints
- [x] Response schema defined for success case
- [x] All error responses documented with status codes and body structure
- [x] Security considerations addressed (user enumeration, timing attacks)
- [x] Authentication flow documented
- [x] Testing scenarios provided
- [x] Backend implementation guidance provided
- [x] Frontend implementation guidance provided
- [x] Password never returned in response
- [x] Consistent error messages for security
- [x] Timing attack prevention specified
