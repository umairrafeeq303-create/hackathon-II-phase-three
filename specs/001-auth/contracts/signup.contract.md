# Contract: User Signup Endpoint

**Endpoint**: `POST /api/auth/signup`
**Version**: v1.0
**Authentication**: Not required
**Purpose**: Register a new user account and return JWT token

## Request

### HTTP Method
```
POST
```

### URL Path
```
/api/auth/signup
```

### Headers
```
Content-Type: application/json
```

### Request Body Schema

```typescript
{
  name: string;      // Required, 1-100 characters, display name
  email: string;     // Required, valid email format (RFC 5322), max 255 characters
  password: string;  // Required, minimum 8 characters
}
```

### Request Body Constraints

| Field | Type | Required | Constraints | Validation |
|-------|------|----------|-------------|------------|
| `name` | string | Yes | 1-100 characters, not empty/whitespace-only | Trim whitespace, check length |
| `email` | string | Yes | Valid email format, max 255 characters, unique | RFC 5322 format, lowercase normalization |
| `password` | string | Yes | Minimum 8 characters | Check length, accept all printable characters |

### Request Example

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePass123!"
}
```

## Response

### Success Response (201 Created)

**Status Code**: `201 Created`

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

### Error 1: Email Already Registered (400 Bad Request)

**Condition**: Email address is already associated with an existing account

**Status Code**: `400 Bad Request`

**Response Body**:
```json
{
  "detail": "Email already registered"
}
```

**Frontend Handling**:
- Display error message: "This email is already registered. Please use a different email or sign in."
- Keep user on signup form with email field highlighted
- Provide link to signin page

---

### Error 2: Invalid Email Format (422 Validation Error)

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
- Show example: "example@domain.com"

---

### Error 3: Password Too Short (422 Validation Error)

**Condition**: Password is less than 8 characters

**Status Code**: `422 Unprocessable Entity`

**Response Body**:
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

**Frontend Handling**:
- Display error message: "Password must be at least 8 characters long."
- Highlight password field
- Show character count indicator

---

### Error 4: Name Too Long (422 Validation Error)

**Condition**: Name exceeds 100 characters

**Status Code**: `422 Unprocessable Entity`

**Response Body**:
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Name must not exceed 100 characters",
      "type": "value_error"
    }
  ]
}
```

**Frontend Handling**:
- Display error message: "Name is too long (maximum 100 characters)."
- Highlight name field
- Show character count: "85/100"

---

### Error 5: Empty Name (422 Validation Error)

**Condition**: Name is empty or whitespace-only

**Status Code**: `422 Unprocessable Entity`

**Response Body**:
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "Name cannot be empty",
      "type": "value_error"
    }
  ]
}
```

**Frontend Handling**:
- Display error message: "Please enter your name."
- Highlight name field

---

### Error 6: Missing Required Fields (422 Validation Error)

**Condition**: One or more required fields are missing from request

**Status Code**: `422 Unprocessable Entity`

**Response Body**:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "password"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Frontend Handling**:
- Display error message: "Please fill in all required fields."
- Highlight all missing fields
- Show field-specific messages for each missing field

---

### Error 7: Database Connection Failed (500 Internal Server Error)

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

### Error 8: Configuration Error (500 Internal Server Error)

**Condition**: BETTER_AUTH_SECRET is missing or invalid

**Status Code**: `500 Internal Server Error`

**Response Body**:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Frontend Handling**:
- Same as Error 7 (generic server error handling)
- Do NOT expose configuration details to user

---

## Security Considerations

### Password Handling

1. **Never Log Plain-Text Passwords**: Backend MUST NOT log the password field from requests
2. **Immediate Hashing**: Password MUST be hashed immediately upon receipt (before any other operations)
3. **Bcrypt Algorithm**: Use bcrypt with minimum 10 salt rounds
4. **No Password in Response**: Password or hashed_password NEVER included in response

### Email Handling

1. **Uniqueness Check**: Database-level unique constraint prevents race conditions
2. **Normalization**: Email converted to lowercase before storage and comparison
3. **Format Validation**: Pydantic EmailStr validates RFC 5322 format

### User Enumeration Prevention

1. **Generic Error Message**: "Email already registered" does not confirm user existence
2. **Consistent Response Time**: No timing difference between "email exists" and "validation error"

### Rate Limiting

**Not implemented in this spec** (out of scope), but production should:
- Limit signup attempts per IP address (e.g., 5 per hour)
- Implement CAPTCHA after failed attempts
- Monitor for suspicious patterns

## Testing

### Valid Request Test Cases

1. **Happy Path**: Valid name, email, password → 201 response with user and token
2. **Special Characters in Name**: Name with unicode characters → 201 response
3. **Special Characters in Password**: Password with symbols → 201 response
4. **Minimum Length Password**: Exactly 8 characters → 201 response
5. **Maximum Length Name**: Exactly 100 characters → 201 response

### Invalid Request Test Cases

1. **Duplicate Email**: Email already registered → 400 error
2. **Invalid Email Format**: "notanemail" → 422 error
3. **Short Password**: 7 characters → 422 error
4. **Empty Name**: "" or "   " → 422 error
5. **Missing Fields**: No email field → 422 error
6. **Long Name**: 101 characters → 422 error

### Error Handling Test Cases

1. **Database Down**: Simulate DB connection failure → 500 error
2. **Invalid Secret**: Simulate missing BETTER_AUTH_SECRET → 500 error (app fails to start)

## Backend Implementation Notes

### Route Handler Signature
```python
@router.post("/signup", status_code=201, response_model=AuthResponse)
async def signup(
    user_create: UserCreate,
    db: Session = Depends(get_db_session)
) -> AuthResponse:
    # Implementation
```

### Implementation Steps
1. Validate request body (automatic via Pydantic)
2. Check if email already exists in database
3. Hash password using bcrypt
4. Create user record in database
5. Generate JWT token with user_id and email
6. Return user information and token

### Error Handling
- `IntegrityError` (duplicate email) → 400 with "Email already registered"
- `ValidationError` (Pydantic) → 422 with field-specific errors
- `Exception` (database/config errors) → 500 with generic message

## Frontend Implementation Notes

### API Client Function
```typescript
async function signup(
  name: string,
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new SignupError(response.status, error.detail);
  }

  return response.json();
}
```

### Form Validation (Client-Side)
- Email format validation (before API call)
- Password length check (minimum 8 characters)
- Name length check (1-100 characters)
- Empty field validation

### Success Handling
1. Store token in localStorage: `localStorage.setItem('auth_token', token)`
2. Update authentication state in React context/store
3. Redirect to `/dashboard` or `/tasks` page
4. Display welcome message with user's name

### Error Handling
- 400 errors: Display field-specific error message
- 422 errors: Display validation error for each field
- 500 errors: Display generic "service unavailable" message with retry option
- Network errors: Display connection error message

## Contract Compliance Checklist

- [x] Request schema defined with all fields and constraints
- [x] Response schema defined for success case
- [x] All error responses documented with status codes and body structure
- [x] Security considerations addressed
- [x] Testing scenarios provided
- [x] Backend implementation guidance provided
- [x] Frontend implementation guidance provided
- [x] Password never returned in response
- [x] Email uniqueness enforced
- [x] Validation rules clearly specified
