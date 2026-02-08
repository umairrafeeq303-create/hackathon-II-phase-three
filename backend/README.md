# Backend - Authentication & User Management System

FastAPI backend for the Todo Application with JWT authentication.

## Prerequisites

- Python 3.11+
- PostgreSQL (via Neon Serverless recommended)
- Virtual environment tool (venv)

## Project Structure

```
backend/
├── src/
│   ├── models/          # SQLModel table definitions
│   ├── schemas/         # Pydantic request/response schemas
│   ├── api/             # FastAPI route handlers
│   ├── core/            # Core utilities (config, security, dependencies)
│   ├── db/              # Database session management
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── alembic/             # Database migration scripts
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md            # This file
```

## Setup Instructions

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies**:
- FastAPI 0.109.0 - Web framework
- Uvicorn 0.27.0 - ASGI server
- SQLModel 0.0.14 - ORM with type safety
- Psycopg2-binary 2.9.9 - PostgreSQL adapter
- Alembic 1.13.1 - Database migrations
- Python-jose 3.3.0 - JWT token handling
- Passlib 1.7.4 - Password hashing (bcrypt)
- Pydantic 2.5.3 - Data validation
- Python-dotenv 1.0.0 - Environment variable management

### Step 3: Configure Environment Variables

Create `.env` file by copying the example:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Database Configuration
# Example for Neon: postgresql://user:pass@ep-cool-name-123456.us-east-1.aws.neon.tech/neondb
DATABASE_URL=postgresql://user:password@localhost:5432/todo_app

# JWT Secret (MUST be the same as frontend BETTER_AUTH_SECRET)
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=your-super-secret-key-minimum-32-characters-long

# CORS Configuration
# Comma-separated list of allowed origins
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.vercel.app

# Environment
ENVIRONMENT=development
```

**Generate a secure secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Set Up Database

#### Option A: Using Alembic (Recommended)

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create users table"

# Apply migration
alembic upgrade head
```

#### Option B: Manual Database Setup

Connect to your PostgreSQL database and run:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Step 5: Run Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in existing user
- `GET /api/auth/me` - Get current user information (requires JWT token)

## Testing

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_auth_signup.py
```

### Run with Coverage

```bash
pytest --cov=src tests/
```

## Testing with cURL

### Signup

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

Expected response (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "name": "Test User",
    "created_at": "2026-01-09T10:30:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Signin

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### Get Current User

```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <your-jwt-token>"
```

## Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

## Common Issues

### Database Connection Failed

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
- Verify `DATABASE_URL` is correct in `.env`
- Check that database is running
- Verify network connectivity
- Check if IP address is allowlisted (for cloud databases like Neon)

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Verify you're in the correct directory

### JWT Token Invalid

**Error**: `401 Unauthorized: Invalid token`

**Solution**:
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check that secret is at least 32 characters
- Verify token is being sent in Authorization header
- Check token hasn't expired (7-day expiry)

### CORS Errors

**Solution**:
- Verify `CORS_ORIGINS` includes frontend URL in `.env`
- Restart backend server after changing CORS configuration
- Check that frontend is using correct API URL

## Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use FastAPI Automatic Docs

Navigate to http://localhost:8000/docs to test endpoints directly in Swagger UI.

### Check Database State

```sql
SELECT * FROM users;
```

## Security

- Passwords are hashed using bcrypt with minimum 10 salt rounds
- JWT tokens expire after 7 days
- JWT tokens use HS256 algorithm
- Email addresses are case-insensitive and stored in lowercase
- CORS is configured to only allow specified origins

## Phase III: AI Chatbot (Natural Language Task Management)

The AI Chatbot feature enables users to manage tasks through natural language conversations powered by OpenAI's GPT-3.5-turbo model.

### Architecture Overview

- **Agent**: OpenAI GPT-3.5-turbo with tool calling
- **Tools**: 5 MCP (Model Context Protocol) tools for task operations
- **Database**: Conversation and Message tables for history
- **Design**: Fully stateless - loads history from database on every request
- **Security**: Multi-layer user ownership validation

### Additional Setup for AI Chatbot

#### 1. Get OpenAI API Key

- Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Create a new secret key
- Copy the key (starts with `sk-proj-...`)

#### 2. Configure Environment Variables

Add to your `.env` file:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Important**: Keep this key secure and never commit it to version control.

#### 3. Install Additional Dependencies

The chatbot requires additional Python packages:

```bash
pip install openai>=1.0.0 mcp>=1.0.0 tenacity>=8.2.0
```

Or reinstall from updated requirements.txt:

```bash
pip install -r requirements.txt
```

**New Dependencies**:
- `openai>=1.0.0` - OpenAI Python SDK with Agents support
- `mcp>=1.0.0` - Model Context Protocol SDK for tool integration
- `tenacity>=8.2.0` - Retry logic for API rate limiting

#### 4. Run Database Migration

The chatbot requires two new tables (`conversations` and `messages`):

```bash
# Apply migration to add chatbot tables
alembic upgrade head
```

**Tables Created**:
- `conversations` - Stores conversation metadata (user_id, created_at, updated_at)
- `messages` - Stores individual messages (conversation_id, role, content, created_at)

**Indexes Created**:
- `idx_conversations_user_id` - Fast conversation lookup by user
- `idx_messages_conversation_id` - Fast message retrieval
- `idx_messages_created_at` - Chronological ordering

#### 5. Verify Setup

Check that everything is configured correctly:

```bash
# Start the backend server
uvicorn src.main:app --reload

# In another terminal, check Swagger docs
curl http://localhost:8000/docs
```

You should see the new chat endpoint: `POST /api/{user_id}/chat`

### AI Chatbot Features

The AI assistant understands natural language and can perform all task operations:

#### Create Tasks
```
User: "Add a task to buy milk"
AI: "Got it! I've added 'Buy milk' to your task list."

User: "I need to remember to call mom tonight"
AI: "Got it! I've added 'Call mom tonight' to your task list."

User: "Create three tasks: milk, eggs, bread"
AI: "I've added these tasks to your list: 1. Milk, 2. Eggs, 3. Bread"
```

#### View Tasks
```
User: "Show me my tasks"
AI: "You have 3 pending tasks: 1. Buy milk, 2. Call mom tonight, 3. Project deadline"

User: "What's pending?"
AI: "You have 2 pending tasks: 1. Buy milk, 2. Call mom tonight"

User: "What have I completed?"
AI: "You've completed 1 task: 1. Finish report"
```

#### Complete Tasks
```
User: "Mark task 1 as complete"
AI: "Great job! I've marked 'Buy milk' as complete."

User: "I finished the groceries"
AI: "Awesome! I've marked 'Buy milk' as complete."
```

#### Delete Tasks
```
User: "Delete task 2"
AI: "I've deleted task 2 from your list."

User: "Remove the meeting task"
AI: "I've deleted 'Team meeting' from your list."
```

#### Update Tasks
```
User: "Change task 1 to 'Buy organic milk'"
AI: "I've updated task 1 to 'Buy organic milk'."

User: "Update the groceries task to include fruits"
AI: "I've updated 'Buy milk' to include fruits in the description."
```

#### Conversation Context
```
User: "Add a task to buy milk"
AI: "Got it! I've added 'Buy milk' to your task list."

User: "Mark that task as complete"  ← References previous message
AI: "Great job! I've marked 'Buy milk' as complete."

User: "Show my tasks"
AI: "You have 2 tasks: 1. Call mom, 2. Project deadline"

User: "Delete the first one"  ← References task from previous list
AI: "I've deleted 'Call mom' from your list."
```

### Key Capabilities

✅ **Natural Language Understanding**: Interprets user intent from conversational input
✅ **Context Awareness**: Remembers previous messages (last 50 messages)
✅ **Reference Resolution**: Understands "that task", "the first one", "it"
✅ **Disambiguation**: Asks for clarification when requests are ambiguous
✅ **Error Recovery**: Provides friendly error messages with suggestions
✅ **User Isolation**: Cannot access other users' tasks (security enforced)
✅ **Stateless Design**: Server restarts don't lose conversation context

### Testing the AI Chatbot

#### Manual Testing via Frontend

1. Start the backend: `uvicorn src.main:app --reload`
2. Navigate to frontend: `http://localhost:3000/chat`
3. Try sample queries:
   - "Add a task to buy groceries"
   - "Show me my tasks"
   - "Mark the first one as complete"

#### Testing via cURL

```bash
# 1. Authenticate
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.access_token')

USER_ID=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.user_id')

# 2. Send chat message
curl -X POST http://localhost:8000/api/$USER_ID/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Add a task to buy groceries"}'

# Expected response:
# {
#   "conversation_id": "uuid-here",
#   "response": "Got it! I've added 'Buy groceries' to your task list.",
#   "tool_calls": [
#     {
#       "tool": "add_task",
#       "parameters": {"user_id": "...", "title": "Buy groceries"},
#       "result": {"task_id": 1, "status": "created", "title": "Buy groceries"}
#     }
#   ]
# }
```

#### Automated Integration Testing

Run the comprehensive integration test suite:

```bash
# Run all Phase 14 integration tests
python3 -m pytest tests/integration_test_phase_14.py -v -s

# Run specific test class
python3 -m pytest tests/integration_test_phase_14.py::TestEndToEndConversations -v

# Run manual interactive tests
python3 tests/manual_test_user_stories.py
```

### MCP Tools (Model Context Protocol)

The chatbot uses 5 stateless tools for task operations:

| Tool | Description | Parameters |
|------|-------------|------------|
| `add_task` | Create a new task | user_id, title, description (optional) |
| `list_tasks` | Retrieve user's tasks | user_id, status (all/pending/completed) |
| `complete_task` | Mark task as done | user_id, task_id |
| `delete_task` | Remove a task | user_id, task_id |
| `update_task` | Modify a task | user_id, task_id, title (optional), description (optional) |

All tools:
- Validate user ownership before operations
- Return standardized response format
- Handle errors gracefully
- Are stateless (no instance variables)

For detailed tool documentation, see `docs/mcp-tools.md`

### Agent Configuration

**Model**: GPT-3.5-turbo
- Cost-effective: $0.002/1K tokens
- Fast response: 1-2 seconds average
- Sufficient accuracy for task management

**System Prompt**: Defines personality and behavior
- Friendly, conversational tone
- Tool selection rules (intent detection)
- Context awareness instructions
- Security constraints
- Error handling guidelines

For full system prompt, see `docs/agent-prompts.md`

### Performance

**Response Time**: < 3 seconds (95th percentile)
- Database query: ~10-50ms (load 50 messages)
- OpenAI API call: 1-2 seconds
- Tool invocation: 5-10ms
- Message storage: 5-10ms

**Concurrency**: Supports 100+ concurrent sessions
- Stateless architecture = horizontal scaling
- Database connection pooling configured
- No in-memory session state

**Rate Limiting**:
- OpenAI API: 3500 RPM (gpt-3.5-turbo)
- Retry logic: Exponential backoff (1s, 2s, 4s)
- Max retries: 3 attempts

### Troubleshooting

#### "Invalid API Key" Error

**Error**: `openai.AuthenticationError: Invalid API key`

**Solution**:
- Verify `OPENAI_API_KEY` in `.env` is correct
- Check key hasn't been revoked at https://platform.openai.com/api-keys
- Ensure key starts with `sk-proj-`
- Restart backend after updating `.env`

#### "Rate Limit Exceeded"

**Error**: `RateLimitError: Rate limit exceeded`

**Solution**:
- The backend automatically retries with exponential backoff
- If persistent, upgrade OpenAI plan or wait for quota reset
- Check current usage at https://platform.openai.com/usage

#### Conversation Not Found

**Error**: `404: Conversation not found`

**Solution**:
- Ensure `conversation_id` is valid and belongs to authenticated user
- Don't try to use other users' conversation IDs
- Start new conversation by omitting `conversation_id` in request

#### AI Not Understanding Requests

**Issue**: AI doesn't correctly interpret user message

**Solution**:
- Be more specific: "Add task to buy milk" vs "Do something with milk"
- Use natural task-related language
- Check system prompt for supported intents in `src/ai/prompts.py`
- Review conversation history - agent may need context

### Monitoring

Track these metrics in production:

- **Response Time**: Monitor p50, p95, p99 latencies
- **OpenAI API Costs**: Track token usage and costs
- **Error Rate**: Monitor 4xx and 5xx responses
- **Tool Success Rate**: Track tool execution failures
- **Conversation Length**: Average messages per conversation

### Documentation

For more information, see:
- **Specification**: `../specs/004-ai-chatbot/spec.md`
- **Implementation Plan**: `../specs/004-ai-chatbot/plan.md`
- **Quickstart Guide**: `../specs/004-ai-chatbot/quickstart.md`
- **MCP Tools**: `docs/mcp-tools.md`
- **Agent Prompts**: `docs/agent-prompts.md`
- **API Contracts**: `../specs/004-ai-chatbot/contracts/`

## Reference Documentation

- Specification: `../specs/001-auth/spec.md`
- Data Model: `../specs/001-auth/data-model.md`
- API Contracts: `../specs/001-auth/contracts/`
- Implementation Plan: `../specs/001-auth/plan.md`
- Quickstart Guide: `../specs/001-auth/quickstart.md`

## External Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Documentation](https://neon.tech/docs)
