# API Documentation Verification Guide

This guide explains how to verify that the Chat API endpoint appears correctly in the Swagger UI documentation.

## Prerequisites

1. Backend server running: `uvicorn src.main:app --reload`
2. Navigate to: http://localhost:8000/docs

## What to Verify (T246)

### 1. Chat Endpoint Visibility

**Expected**: You should see the following endpoint in Swagger UI:

```
POST /api/{user_id}/chat
```

**Location**: Under the "Chat" or default tag section

**Path Parameters**:
- `user_id` (required, string, format: uuid) - User ID from JWT token

### 2. Request Schema

**Expected Request Body**:

```json
{
  "message": "string (max 10000 chars)",
  "conversation_id": "string (uuid) or null"
}
```

**Schema Name**: `ChatRequest`

**Fields**:
- `message` (required): User's chat message
  - Type: string
  - Min length: 1
  - Max length: 10,000
  - Example: "Add a task to buy milk"

- `conversation_id` (optional): Existing conversation UUID
  - Type: string (uuid format) or null
  - Example: "550e8400-e29b-41d4-a716-446655440000"
  - Description: "Omit for new conversation, provide for continuing existing conversation"

### 3. Response Schema

**Expected Response** (200 OK):

```json
{
  "conversation_id": "uuid",
  "response": "string",
  "tool_calls": [
    {
      "tool": "string",
      "parameters": {},
      "result": {}
    }
  ]
}
```

**Schema Name**: `ChatResponse`

**Fields**:
- `conversation_id` (required): UUID of the conversation
  - Type: string (uuid format)
  - Description: "Use this ID in subsequent messages to continue conversation"

- `response` (required): AI assistant's response
  - Type: string
  - Example: "Got it! I've added 'Buy milk' to your task list."

- `tool_calls` (required): Array of tool invocations
  - Type: array of ToolCall objects
  - Default: []
  - Description: "Tools used to fulfill the request (for transparency)"

**ToolCall Schema**:
```json
{
  "tool": "string",          // Tool name: add_task, list_tasks, etc.
  "parameters": {},          // Tool input parameters
  "result": {}               // Tool execution result
}
```

### 4. Security

**Authentication Required**: Yes

**Security Scheme**: Bearer Token (JWT)

**Header**: `Authorization: Bearer <jwt-token>`

**Expected in Swagger**:
- Padlock icon 🔒 next to the endpoint
- "Authorize" button at top of Swagger UI
- Security requirement: `HTTPBearer`

### 5. Error Responses

**Expected Error Responses**:

**400 Bad Request**:
```json
{
  "detail": "Message too long (max 10,000 characters)"
}
```

**401 Unauthorized**:
```json
{
  "detail": "Not authenticated"
}
```

**403 Forbidden**:
```json
{
  "detail": "Forbidden - user_id mismatch"
}
```

**404 Not Found**:
```json
{
  "detail": "Conversation not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "I'm having trouble saving your message. Please try again."
}
```

## Testing via Swagger UI

### Step 1: Authenticate

1. Click "Authorize" button at top of Swagger UI
2. Enter JWT token: `Bearer <your-token-here>`
3. Click "Authorize" then "Close"

### Step 2: Test Chat Endpoint

1. Expand `POST /api/{user_id}/chat`
2. Click "Try it out"
3. Fill in parameters:
   - `user_id`: Your user UUID (from login response)
   - Request body:
     ```json
     {
       "message": "Add a task to buy milk"
     }
     ```
4. Click "Execute"

### Step 3: Verify Response

**Expected** (200 OK):
```json
{
  "conversation_id": "some-uuid-here",
  "response": "Got it! I've added 'Buy milk' to your task list.",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "your-user-uuid",
        "title": "Buy milk"
      },
      "result": {
        "task_id": 1,
        "status": "created",
        "title": "Buy milk"
      }
    }
  ]
}
```

### Step 4: Continue Conversation

1. Keep the endpoint expanded
2. Click "Try it out" again
3. Fill in parameters:
   - `user_id`: Same as before
   - Request body:
     ```json
     {
       "message": "Show me my tasks",
       "conversation_id": "uuid-from-previous-response"
     }
     ```
4. Click "Execute"

**Expected**: AI lists the task you just created

## Verification Checklist

Use this checklist to verify API documentation (T246):

- [ ] Swagger UI accessible at `/docs`
- [ ] Chat endpoint visible: `POST /api/{user_id}/chat`
- [ ] Endpoint has 🔒 security indicator
- [ ] `user_id` path parameter documented
- [ ] `ChatRequest` schema visible in request body
  - [ ] `message` field (required, string, max 10000)
  - [ ] `conversation_id` field (optional, uuid)
- [ ] `ChatResponse` schema visible in responses
  - [ ] `conversation_id` field (uuid)
  - [ ] `response` field (string)
  - [ ] `tool_calls` field (array)
- [ ] `ToolCall` schema documented
  - [ ] `tool` field
  - [ ] `parameters` field
  - [ ] `result` field
- [ ] Error responses documented (400, 401, 403, 404, 500)
- [ ] "Try it out" functionality works
- [ ] Authentication via "Authorize" button works
- [ ] Example request/response provided

## Common Issues

### Chat Endpoint Not Visible

**Cause**: Router not registered in `main.py`

**Solution**:
```python
# backend/src/main.py
from src.api.routes.chat import router as chat_router

app.include_router(chat_router)
```

### Security Not Showing

**Cause**: Missing security dependency in route

**Solution**:
```python
# backend/src/api/routes/chat.py
@router.post("/{user_id}/chat", dependencies=[Depends(get_current_user_id)])
```

### Schema Not Displayed

**Cause**: Missing Pydantic examples

**Solution**:
```python
# backend/src/schemas/chat.py
class ChatRequest(BaseModel):
    message: str = Field(..., max_length=10000, example="Add a task to buy milk")
    conversation_id: Optional[str] = Field(None, example="550e8400-e29b-41d4-a716-446655440000")
```

### ToolCall Schema Missing

**Cause**: Not defined or not referenced

**Solution**:
```python
class ToolCall(BaseModel):
    tool: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall] = []
```

## Screenshot Locations

For documentation purposes, capture screenshots of:

1. Swagger UI homepage showing chat endpoint
2. Expanded chat endpoint with request/response schemas
3. "Try it out" with example request
4. Successful response with tool_calls

Save screenshots to: `backend/docs/screenshots/`

## Additional Verification

### ReDoc Alternative

Navigate to: http://localhost:8000/redoc

**Benefits**:
- Three-column layout
- Better for reading complex schemas
- Search functionality
- Easier navigation

**Verify**:
- Chat endpoint appears in left sidebar
- Schemas well-formatted
- Examples visible

### OpenAPI JSON

Download OpenAPI spec: http://localhost:8000/openapi.json

**Verify**:
```json
{
  "paths": {
    "/api/{user_id}/chat": {
      "post": {
        "summary": "...",
        "requestBody": {...},
        "responses": {...},
        "security": [{"HTTPBearer": []}]
      }
    }
  }
}
```

## Automated Verification

Create a test to verify API documentation:

```python
import requests

def test_openapi_schema():
    """Verify chat endpoint in OpenAPI schema."""
    response = requests.get("http://localhost:8000/openapi.json")
    schema = response.json()

    # Verify endpoint exists
    assert "/api/{user_id}/chat" in schema["paths"]

    # Verify method
    endpoint = schema["paths"]["/api/{user_id}/chat"]
    assert "post" in endpoint

    # Verify request schema
    assert "requestBody" in endpoint["post"]

    # Verify response schema
    assert "responses" in endpoint["post"]
    assert "200" in endpoint["post"]["responses"]
```

## Conclusion

The API documentation in Swagger UI provides:
- ✅ Interactive testing interface
- ✅ Complete request/response schemas
- ✅ Authentication examples
- ✅ Error response documentation
- ✅ Try-it-out functionality

This enables developers to:
- Understand the API without reading code
- Test endpoints directly in browser
- Generate client SDKs
- Share API contracts with frontend team
