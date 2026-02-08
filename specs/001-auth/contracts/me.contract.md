# Contract: Get Current User Endpoint

**Endpoint**: `GET /api/auth/me`
**Version**: v1.0
**Authentication**: Required (JWT token)
**Purpose**: Retrieve authenticated user's information

## Request

### HTTP Method
```
GET
```

### URL Path
```
/api/auth/me
```

### Headers
```
Authorization: Bearer <jwt_token>
```

**Required Header**: `Authorization` with value `Bearer <token>` where `<token>` is a valid JWT token obtained from signup or signin.

### Request Body
```
None (GET request has no body)
```

### Query Parameters
```
None
```

### Request Example

```http
GET /api/auth/me HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTUwZTg0MDAtZTI5Yi00MWQ0LWE3MTYtNDQ2NjU1NDQwMDAwIiwiZW1haWwiOiJqb2huLmRvZUBleGFtcGxlLmNvbSIsImV4cCI6MTczNjUwMDIwMCwiaWF0IjoxNzM1ODk1NDAwfQ.signature_here
```

## Response

### Success Response (200 OK)

**Status Code**: `200 OK`

**Response Body Schema**:
```typescript
{
  id: string;         // UUID v4 format
  email: string;      // User's email (lowercase)
  name: string;       // User's display name
  created_at: string; // ISO 8601 datetime (UTC)
}
```

**Note**: Response does NOT include JWT token (only user information).

**Response Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "created_at": "2026-01-09T10:30:00Z"
}
```

**Response Headers**:
```
Content-Type: application/json
```

**Use Cases**:
1. Display user's name in UI header/navigation
2. Pre-fill user profile forms
3. Verify authentication state on page load
4. Display user's email in account settings

---

## Error Responses

### Error 1: Missing Authorization Header (401 Unauthorized)

**Condition**: Request does not include Authorization header

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Authorization header required"
}
```

**Frontend Handling**:
- Clear any stored token (invalid state)
- Redirect to signin page
- Display message: "Please sign in to continue."

---

### Error 2: Malformed Authorization Header (401 Unauthorized)

**Condition**: Authorization header is not in "Bearer <token>" format

**Examples**:
- `Authorization: <token>` (missing "Bearer" prefix)
- `Authorization: Bearer` (missing token)
- `Authorization: Token <token>` (wrong prefix)

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Invalid token"
}
```

**Frontend Handling**:
- Clear stored token (corrupted)
- Redirect to signin page
- Log error for debugging

---

### Error 3: Invalid JWT Token (401 Unauthorized)

**Condition**: Token signature is invalid or token is malformed

**Causes**:
- Token was tampered with
- Token was signed with different secret
- Token is not a valid JWT format

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Invalid token"
}
```

**Frontend Handling**:
- Clear stored token
- Redirect to signin page
- Display message: "Your session is invalid. Please sign in again."

---

### Error 4: Expired JWT Token (401 Unauthorized)

**Condition**: Token's `exp` (expiration) timestamp is in the past

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Token expired"
}
```

**Frontend Handling**:
- Clear stored token
- Redirect to signin page
- Display message: "Your session has expired. Please sign in again."
- Consider: Offer "Remember me" option during next signin

---

### Error 5: User Not Found (401 Unauthorized)

**Condition**: Token is valid but user_id from token does not exist in database

**Causes**:
- User account was deleted after token was issued
- Database inconsistency

**Status Code**: `401 Unauthorized`

**Response Body**:
```json
{
  "detail": "Invalid token"
}
```

**Frontend Handling**:
- Clear stored token
- Redirect to signin page
- Display message: "Your account was not found. Please sign in again or contact support."

---

### Error 6: Database Connection Failed (500 Internal Server Error)

**Condition**: Backend cannot connect to database to fetch user information

**Status Code**: `500 Internal Server Error`

**Response Body**:
```json
{
  "detail": "Service temporarily unavailable"
}
```

**Frontend Handling**:
- Display error message: "Service temporarily unavailable. Please try again."
- Keep user on current page
- Provide retry button
- Do NOT clear token (token is valid, database is just temporarily down)

---

## Security Considerations

### JWT Token Validation

Backend MUST perform all validation steps:
1. Extract token from Authorization header
2. Verify token signature using BETTER_AUTH_SECRET
3. Check token expiration (`exp` < current_time)
4. Extract `user_id` from token payload
5. Verify user exists in database

### Token Leakage Prevention

1. **HTTPS Only**: Token MUST only be transmitted over HTTPS in production
2. **No URL Parameters**: Token MUST NOT be in URL (only in Authorization header)
3. **No Logging**: Token MUST NOT be logged by backend
4. **Short-Lived**: Token expires after 7 days (limited blast radius)

### CORS Configuration

Backend MUST:
- Allow Authorization header
- Allow credentials
- Allow requests only from configured frontend origin

## Authentication Dependency Pattern

### Backend Implementation (FastAPI Dependency)

```python
# Conceptual implementation - not production code
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    FastAPI dependency that extracts and validates JWT token.
    Returns user_id if token is valid, raises 401 error otherwise.
    """
    token = credentials.credentials

    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        # Extract user_id from payload
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Route Handler Usage

```python
@router.get("/me", status_code=200, response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db_session)
) -> UserResponse:
    """Get authenticated user's information"""

    # Query database for user
    user = db.get(User, current_user_id)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user
```

## Testing

### Valid Request Test Cases

1. **Happy Path**: Valid token → 200 response with user information
2. **Recently Created User**: Token from signup → 200 response
3. **Token Near Expiry**: Token with exp = current_time + 1 second → 200 response

### Invalid Request Test Cases

1. **Missing Authorization Header**: No header → 401 "Authorization header required"
2. **Malformed Header**: `Authorization: <token>` (no Bearer) → 401 "Invalid token"
3. **Empty Token**: `Authorization: Bearer` → 401 "Invalid token"
4. **Invalid Signature**: Token signed with wrong secret → 401 "Invalid token"
5. **Expired Token**: Token with exp = current_time - 1 second → 401 "Token expired"
6. **Tampered Token**: Modified payload → 401 "Invalid token"
7. **Non-Existent User**: Valid token but user deleted → 401 "Invalid token"
8. **Wrong Algorithm**: Token signed with RS256 instead of HS256 → 401 "Invalid token"

### Security Test Cases

1. **Token Reuse**: Same token used multiple times → All requests succeed (tokens are stateless)
2. **CORS Validation**: Request from unauthorized origin → Blocked by CORS
3. **HTTPS Enforcement**: HTTP request in production → Rejected (infrastructure level)

### Error Handling Test Cases

1. **Database Down**: Simulate DB connection failure → 500 error
2. **User Query Failure**: Simulate query error → 500 error

## Frontend Implementation Notes

### API Client Function

```typescript
async function getCurrentUser(): Promise<User> {
  const token = localStorage.getItem('auth_token');

  if (!token) {
    throw new Error('No authentication token found');
  }

  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (response.status === 401) {
    // Token is invalid or expired - clear it
    localStorage.removeItem('auth_token');
    throw new AuthenticationError('Session expired');
  }

  if (!response.ok) {
    throw new Error('Failed to fetch user information');
  }

  return response.json();
}
```

### Usage in React Components

```typescript
// Example: Fetch user on app initialization
useEffect(() => {
  const fetchUser = async () => {
    try {
      const user = await getCurrentUser();
      setUser(user);
      setIsAuthenticated(true);
    } catch (error) {
      if (error instanceof AuthenticationError) {
        // Redirect to signin page
        router.push('/signin');
      } else {
        // Show error message
        setError('Failed to load user information');
      }
    }
  };

  fetchUser();
}, []);
```

### Protected Route Pattern

```typescript
// Example: Protected page component
export default function DashboardPage() {
  const { user, isLoading } = useAuth(); // Custom hook that calls getCurrentUser

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!user) {
    redirect('/signin');
  }

  return (
    <div>
      <h1>Welcome, {user.name}!</h1>
      {/* Dashboard content */}
    </div>
  );
}
```

### Error Handling Strategy

| Status Code | Action | User Message |
|-------------|--------|--------------|
| 401 | Clear token, redirect to signin | "Your session has expired. Please sign in again." |
| 500 | Show error, keep on page | "Service temporarily unavailable. Please try again." |
| Network error | Show error, provide retry | "Connection error. Please check your internet connection." |

### Caching Considerations

- **Cache User Data**: Store user info in React context/state to avoid repeated API calls
- **Invalidate on Logout**: Clear cached user data when user logs out
- **Invalidate on 401**: Clear cached user data when token is invalid
- **Refresh Strategy**: Re-fetch user data after token refresh (if implemented)

## Performance Considerations

### Backend Performance

- **Database Query**: O(1) lookup via primary key (user_id)
- **JWT Verification**: ~1-5ms (signature validation)
- **Total Latency**: <50ms (as specified in SC-004)

### Frontend Performance

- **Initial Load**: Fetch user on app initialization (one-time cost)
- **Subsequent Requests**: Use cached user data from context/state
- **Protected Routes**: Check cached user data (no API call)

### Optimization Strategies

1. **Context/State Management**: Cache user info in React context
2. **Parallel Requests**: Fetch user and other data concurrently
3. **Prefetching**: Fetch user during signin response processing
4. **Error Boundaries**: Graceful error handling for failed requests

## Contract Compliance Checklist

- [x] Request format defined (GET with Authorization header)
- [x] Response schema defined for success case
- [x] All error responses documented with status codes and body structure
- [x] Security considerations addressed (JWT validation, token leakage)
- [x] Authentication dependency pattern documented
- [x] Testing scenarios provided
- [x] Backend implementation guidance provided
- [x] Frontend implementation guidance provided
- [x] Password never returned in response
- [x] Token validation steps clearly specified
- [x] Error handling strategy defined
- [x] Performance characteristics documented
