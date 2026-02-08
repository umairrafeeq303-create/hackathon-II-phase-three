# Task CRUD Agent Skills

## 1. FastAPI Route Handlers
- Path parameters
- Query parameters
- Request body parsing
- Response models
- Status codes

## 2. Pydantic Models
- TaskCreate schema
- TaskUpdate schema
- TaskResponse schema
- Validation rules
- Custom validators

## 3. SQLModel Queries
- Filter by user_id
- Filter by status
- Sorting (order_by)
- Single record fetch
- Multiple records fetch

## 4. Authentication Integration
- Dependency on JWT verification
- Extract user from token
- Validate user_id match
- Protected route patterns

## 5. CRUD Logic
- Create with user association
- Read with ownership check
- Update with ownership check
- Delete with ownership check
- Partial updates (PATCH)

## 6. Data Validation
- Input sanitization
- Length constraints
- Required fields
- Optional fields
- Type checking

## 7. Error Responses
- 404 Not Found
- 403 Forbidden
- 422 Validation Error
- 500 Server Error
- Custom error messages

## 8. Database Transactions
- Commit on success
- Rollback on error
- Async operations
- Session management