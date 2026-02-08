# Quickstart Guide: Todo AI Chatbot

**Feature**: 004-ai-chatbot
**Date**: 2026-01-27
**Estimated Setup Time**: 15 minutes

## Prerequisites

**Phase II Completion** (REQUIRED):
- ✅ Backend running on Railway with DATABASE_URL configured
- ✅ Frontend running on Vercel with authentication working
- ✅ User registration and JWT authentication functional
- ✅ Task CRUD API endpoints operational
- ✅ Neon PostgreSQL database accessible

**Required Accounts**:
- OpenAI account with API access ([https://platform.openai.com](https://platform.openai.com))
- Active OpenAI API key (starts with `sk-`)

**Verification Commands**:
```bash
# Verify Phase II backend running
curl http://localhost:8000/docs

# Verify database connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users;"

# Verify frontend running
curl http://localhost:3000
```

## Backend Setup

### 1. Install Dependencies

```bash
cd backend

# Add to requirements.txt
openai>=1.0.0
mcp>=1.0.0
tenacity>=8.2.0  # For retry logic

# Install
pip install -r requirements.txt

# Or install directly
pip install openai mcp tenacity
```

### 2. Configure Environment Variables

Add to `backend/.env`:
```bash
# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
CORS_ORIGINS=http://localhost:3000

# NEW for Phase III
OPENAI_API_KEY=sk-...your-key-here
```

**Get OpenAI API Key**:
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy key (starts with `sk-`)
4. Paste into `.env`

⚠️ **Security**: Never commit `.env` to git. Verify `.env` is in `.gitignore`.

### 3. Run Database Migration

```bash
cd backend

# Generate migration
alembic revision --autogenerate -m "Add conversation and message tables"

# Review generated migration
cat alembic/versions/*_add_conversation_and_message_tables.py

# Apply migration
alembic upgrade head

# Verify tables created
psql $DATABASE_URL -c "\d conversations"
psql $DATABASE_URL -c "\d messages"
```

**Expected output**:
```
conversations | table | owner
messages      | table | owner
```

### 4. Start Backend Server

```bash
cd backend

# Development
uvicorn src.main:app --reload --port 8000

# Production (Railway)
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

**Verify**:
- Visit [http://localhost:8000/docs](http://localhost:8000/docs)
- Look for `POST /api/{user_id}/chat` endpoint

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend

# Add to package.json dependencies
npm install @openai/chatkit

# Or install directly
npm install @openai/chatkit
```

### 2. Verify Environment Variables

Check `frontend/.env.local`:
```bash
# Existing from Phase II
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=...same-as-backend...

# No new variables needed for frontend
```

### 3. Start Frontend Server

```bash
cd frontend

# Development
npm run dev

# Visit http://localhost:3000
```

## Testing the Chat bot

### Test 1: Create Task via Natural Language

**Prerequisites**: User must be registered and logged in.

**Steps**:
1. Navigate to `/chat` route
2. Type: "Add a task to buy groceries"
3. Press Send

**Expected Result**:
```
AI: Got it! I've added 'Buy groceries' to your task list.
```

**Verification**:
```bash
# Check task created in database
psql $DATABASE_URL -c "SELECT * FROM tasks WHERE title = 'Buy groceries';"
```

### Test 2: View Tasks

**Steps**:
1. Type: "Show me my tasks"
2. Press Send

**Expected Result**:
```
AI: You have 1 pending task: 1. Buy groceries
```

### Test 3: Complete Task

**Steps**:
1. Type: "Mark task 1 as complete"
2. Press Send

**Expected Result**:
```
AI: Great job! I've marked 'Buy groceries' as complete.
```

**Verification**:
```bash
# Check task completed
psql $DATABASE_URL -c "SELECT completed FROM tasks WHERE id = 1;"
# Should return: t (true)
```

### Test 4: Conversation Context

**Steps**:
1. Type: "Add a task to buy milk"
2. Wait for response
3. Type: "Mark that task as complete" (referencing previous message)
4. Press Send

**Expected Result**:
```
AI: Got it! I've added 'Buy milk' to your task list.
AI: Great job! I've marked 'Buy milk' as complete.
```

**Verification**: AI correctly identifies "that task" as the milk task from context.

### Test 5: Server Restart (Stateless Validation)

**Steps**:
1. Start a conversation, send 2-3 messages
2. Restart backend server: `Ctrl+C` and `uvicorn src.main:app --reload`
3. Send another message in the same conversation

**Expected Result**: AI maintains full conversation context, references earlier messages correctly.

**Verification**: No "conversation reset" or context loss after restart.

## Troubleshooting

### Issue: "OpenAI API key not found"

**Cause**: OPENAI_API_KEY not set in environment
**Solution**:
```bash
# Check if key is set
echo $OPENAI_API_KEY

# Set temporarily
export OPENAI_API_KEY=sk-...

# Add to .env permanently
echo "OPENAI_API_KEY=sk-..." >> backend/.env
```

### Issue: "RateLimitError: You exceeded your current quota"

**Cause**: OpenAI API quota exceeded or payment method required
**Solution**:
1. Visit [https://platform.openai.com/account/billing](https://platform.openai.com/account/billing)
2. Add payment method
3. Check usage limits

### Issue: "Conversation not found"

**Cause**: conversation_id from previous session invalid or belongs to different user
**Solution**:
- Frontend should create new conversation (omit conversation_id in request)
- Check localStorage for stale conversation_id and clear if needed

### Issue: Migration fails with "table already exists"

**Cause**: Tables created manually or migration run twice
**Solution**:
```bash
# Check migration status
alembic current

# If needed, mark migration as applied
alembic stamp head

# Or drop tables and re-run
psql $DATABASE_URL -c "DROP TABLE IF EXISTS messages CASCADE;"
psql $DATABASE_URL -c "DROP TABLE IF EXISTS conversations CASCADE;"
alembic upgrade head
```

### Issue: Database query slow (>3s response time)

**Cause**: Missing indexes or large message history
**Solution**:
```bash
# Verify indexes exist
psql $DATABASE_URL -c "\d messages"
# Should show idx_messages_conversation_id and idx_messages_created_at

# Create missing indexes
psql $DATABASE_URL -c "CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);"
psql $DATABASE_URL -c "CREATE INDEX idx_messages_created_at ON messages(created_at);"
```

### Issue: CORS error from frontend

**Cause**: Frontend origin not in CORS_ORIGINS
**Solution**:
```bash
# Update backend/.env
CORS_ORIGINS=http://localhost:3000,https://your-vercel-domain.vercel.app
```

## Deployment to Production

### Railway (Backend)

**Environment Variables**:
```
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
CORS_ORIGINS=https://your-vercel-domain.vercel.app
OPENAI_API_KEY=sk-...
```

**Deployment**:
```bash
git add .
git commit -m "Add Phase III AI chatbot backend"
git push origin main
# Railway auto-deploys from main branch
```

**Run Migration**:
```bash
# SSH into Railway or use Railway CLI
railway run alembic upgrade head
```

### Vercel (Frontend)

**Environment Variables**: No new variables needed (OPENAI_API_KEY is backend-only)

**Deployment**:
```bash
git add .
git commit -m "Add Phase III AI chatbot frontend"
git push origin main
# Vercel auto-deploys from main branch
```

## Monitoring and Maintenance

**OpenAI API Usage**:
- Monitor at [https://platform.openai.com/usage](https://platform.openai.com/usage)
- Set up billing alerts
- Track token consumption

**Database Storage**:
- Monitor conversation count: `SELECT COUNT(*) FROM conversations;`
- Monitor message count: `SELECT COUNT(*) FROM messages;`
- Implement conversation archival if storage grows (out of scope for MVP)

**Performance Monitoring**:
```python
# Add to chat endpoint
import time
start = time.time()
# ... process request ...
duration = time.time() - start
print(f"Chat request took {duration:.2f}s")
```

## Next Steps

After successful testing:
1. ✅ Backend and frontend running with chat interface
2. → Run `/sp.tasks` to generate implementation task breakdown
3. → Execute `/sp.implement` to build the feature
4. → Deploy to production (Railway + Vercel)
5. → Monitor OpenAI API usage and costs

## Support Resources

- OpenAI API Docs: [https://platform.openai.com/docs](https://platform.openai.com/docs)
- OpenAI Agents SDK: [https://github.com/openai/openai-agents-sdk](https://github.com/openai/openai-agents-sdk)
- MCP SDK: [https://github.com/modelcontextprotocol/sdk](https://github.com/modelcontextprotocol/sdk)
- SQLModel Docs: [https://sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- FastAPI Docs: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
