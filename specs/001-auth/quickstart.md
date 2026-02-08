# Quickstart Guide: Authentication & User Management System

**Feature**: 001-auth
**Date**: 2026-01-09
**Audience**: Developers implementing the authentication system

## Overview

This guide provides step-by-step instructions for implementing and testing the Authentication & User Management System. Follow these instructions to set up the backend (FastAPI) and frontend (Next.js) authentication components.

## Prerequisites

### Required Tools

- **Python**: 3.11+ (backend)
- **Node.js**: 20+ (frontend)
- **PostgreSQL**: Via Neon Serverless (cloud-hosted)
- **Git**: For version control
- **Code Editor**: VS Code recommended

### Required Accounts

- **Neon Database**: Sign up at [neon.tech](https://neon.tech) for PostgreSQL hosting
- **Vercel** (optional): For frontend deployment
- **Railway** (optional): For backend deployment

### Environment Setup

Ensure you have the following installed:
```bash
# Check Python version
python --version  # Should be 3.11 or higher

# Check Node.js version
node --version    # Should be 20 or higher

# Check npm version
npm --version     # Should be 10 or higher
```

## Project Structure

```
todo-app-phase-||/
├── backend/                     # FastAPI application
│   ├── src/
│   │   ├── models/
│   │   │   └── user.py         # User SQLModel definition
│   │   ├── schemas/
│   │   │   └── auth.py         # Pydantic request/response schemas
│   │   ├── api/
│   │   │   └── auth.py         # Authentication endpoints
│   │   ├── core/
│   │   │   ├── config.py       # Environment configuration
│   │   │   ├── security.py     # Password hashing and JWT utilities
│   │   │   └── deps.py         # FastAPI dependencies
│   │   ├── db/
│   │   │   └── session.py      # Database session management
│   │   └── main.py             # FastAPI app entry point
│   ├── tests/
│   │   ├── test_auth_signup.py
│   │   ├── test_auth_signin.py
│   │   └── test_auth_me.py
│   ├── alembic/                # Database migrations
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variable template
│   └── README.md
│
├── frontend/                    # Next.js application
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/
│   │   │   │   ├── signup/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── signin/
│   │   │   │       └── page.tsx
│   │   │   └── layout.tsx
│   │   ├── lib/
│   │   │   ├── api.ts          # API client
│   │   │   └── auth.ts         # Better Auth configuration
│   │   ├── components/
│   │   │   └── auth/
│   │   │       ├── SignupForm.tsx
│   │   │       └── SigninForm.tsx
│   │   └── types/
│   │       └── auth.ts         # TypeScript interfaces
│   ├── package.json
│   ├── .env.local.example      # Environment variable template
│   └── README.md
│
└── specs/                       # Feature specifications
    └── 001-auth/
        ├── spec.md              # Requirements specification
        ├── plan.md              # Implementation plan
        ├── research.md          # Research phase output
        ├── data-model.md        # Database schema and models
        ├── quickstart.md        # This file
        └── contracts/           # API contract definitions
```

## Backend Setup

### Step 1: Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt** content:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.3
python-dotenv==1.0.0
```

### Step 2: Set Up Environment Variables

Create `.env` file in `backend/` directory:

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
```

**.env** content:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host:5432/dbname
# Example from Neon: postgresql://user:pass@ep-cool-name-123456.us-east-1.aws.neon.tech/neondb

# JWT Configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long
# Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,https://your-frontend-domain.vercel.app

# Environment
ENVIRONMENT=development
```

**Important**: Generate a strong `BETTER_AUTH_SECRET`:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Set Up Database

#### Option A: Create Database with Alembic (Recommended)

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create users table"

# Apply migration
alembic upgrade head
```

#### Option B: Create Database Manually

```sql
-- Connect to your Neon database and run:
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    hashed_password VARCHAR(60) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Step 4: Run Backend Server

```bash
# Start development server with hot reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Step 5: Test Backend Endpoints

#### Test Signup Endpoint

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

#### Test Signin Endpoint

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

#### Test Get Current User Endpoint

```bash
# Replace <token> with the JWT token from signup/signin response
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer <token>"
```

---

## Frontend Setup

### Step 1: Install Node.js Dependencies

```bash
cd frontend

# Install dependencies
npm install
```

**package.json** dependencies:
```json
{
  "dependencies": {
    "next": "^16.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "typescript": "^5.3.3",
    "tailwindcss": "^3.4.1",
    "better-auth": "^1.0.0"
  }
}
```

### Step 2: Set Up Environment Variables

Create `.env.local` file in `frontend/` directory:

```bash
# Copy example file
cp .env.local.example .env.local

# Edit .env.local with your values
```

**.env.local** content:
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Secret (MUST match backend secret exactly)
BETTER_AUTH_SECRET=your-super-secret-key-min-32-characters-long
```

**Critical**: Use the EXACT same `BETTER_AUTH_SECRET` as the backend.

### Step 3: Configure Better Auth

Create `src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },
  plugins: {
    jwt: {
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d",
    },
  },
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL!,
  },
});
```

### Step 4: Create API Client

Create `src/lib/api.ts`:

```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface AuthResponse {
  user: User;
  token: string;
}

export class AuthError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "AuthError";
  }
}

export async function signup(
  name: string,
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new AuthError(response.status, error.detail);
  }

  return response.json();
}

export async function signin(
  email: string,
  password: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/signin`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new AuthError(response.status, error.detail);
  }

  return response.json();
}

export async function getCurrentUser(): Promise<User> {
  const token = localStorage.getItem("auth_token");

  if (!token) {
    throw new AuthError(401, "No authentication token found");
  }

  const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 401) {
    localStorage.removeItem("auth_token");
    throw new AuthError(401, "Session expired");
  }

  if (!response.ok) {
    throw new Error("Failed to fetch user information");
  }

  return response.json();
}

export function logout(): void {
  localStorage.removeItem("auth_token");
}
```

### Step 5: Run Frontend Development Server

```bash
# Start development server
npm run dev
```

Server will be available at:
- **Frontend**: http://localhost:3000

### Step 6: Test Frontend

1. Navigate to http://localhost:3000/auth/signup
2. Fill in the signup form
3. Submit the form
4. Verify you're redirected to the dashboard
5. Check localStorage for `auth_token`

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth_signup.py

# Run with coverage
pytest --cov=src tests/
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Manual Testing Checklist

#### Signup Flow
- [ ] Create account with valid inputs → Success (201)
- [ ] Try duplicate email → Error "Email already registered" (400)
- [ ] Try short password (7 chars) → Error "Password must be at least 8 characters" (422)
- [ ] Try invalid email format → Error "Invalid email format" (422)
- [ ] Verify JWT token is returned
- [ ] Verify JWT token is stored in localStorage
- [ ] Verify redirect to dashboard

#### Signin Flow
- [ ] Sign in with correct credentials → Success (200)
- [ ] Try wrong password → Error "Invalid credentials" (401)
- [ ] Try non-existent email → Error "Invalid credentials" (401)
- [ ] Verify JWT token is returned
- [ ] Verify JWT token is stored in localStorage
- [ ] Verify redirect to dashboard

#### Protected Routes
- [ ] Access /api/auth/me with valid token → Success (200)
- [ ] Access /api/auth/me without token → Error "Authorization header required" (401)
- [ ] Access /api/auth/me with invalid token → Error "Invalid token" (401)
- [ ] Access /api/auth/me with expired token → Error "Token expired" (401)

#### Logout Flow
- [ ] Click logout button → Token removed from localStorage
- [ ] Verify redirect to signin page
- [ ] Try to access protected route → Redirected to signin

---

## Common Issues and Solutions

### Issue 1: Database Connection Failed

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
- Verify `DATABASE_URL` is correct in `.env`
- Check that Neon database is running
- Verify network connectivity
- Check if IP address is allowlisted in Neon dashboard

### Issue 2: JWT Token Invalid

**Error**: `401 Unauthorized: Invalid token`

**Solution**:
- Verify `BETTER_AUTH_SECRET` matches between frontend and backend
- Check that secret is at least 32 characters
- Verify token is being sent in Authorization header
- Check token hasn't expired (7-day expiry)

### Issue 3: CORS Errors

**Error**: `Access to fetch at '...' from origin '...' has been blocked by CORS policy`

**Solution**:
- Verify `CORS_ORIGINS` includes frontend URL in backend `.env`
- Restart backend server after changing CORS configuration
- Check that frontend is using correct API URL

### Issue 4: Module Not Found (Backend)

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Verify you're in the correct directory

### Issue 5: Module Not Found (Frontend)

**Error**: `Module not found: Can't resolve 'better-auth'`

**Solution**:
- Run `npm install` in frontend directory
- Delete `node_modules` and `package-lock.json`, then run `npm install` again
- Verify you're using Node.js 20+

---

## Development Tips

### Debugging Backend

1. **Enable Debug Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Use FastAPI Automatic Docs**:
   - Navigate to http://localhost:8000/docs
   - Test endpoints directly in Swagger UI

3. **Check Database State**:
   ```sql
   SELECT * FROM users;
   ```

### Debugging Frontend

1. **Check Browser Console**: Press F12 to open DevTools
2. **Inspect Network Requests**: Check Network tab for API calls
3. **Check localStorage**: Application tab → Local Storage
4. **React DevTools**: Install React DevTools browser extension

### Hot Reload

- **Backend**: Use `--reload` flag with uvicorn (automatically enabled)
- **Frontend**: Next.js automatically reloads on file changes

### Database Migrations

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

---

## Next Steps

After completing the quickstart:

1. **Review Contracts**: Read contract files in `specs/001-auth/contracts/`
2. **Implement Frontend UI**: Create signup and signin pages (see Spec 3)
3. **Add Error Handling**: Improve error messages and user feedback
4. **Write Tests**: Add unit and integration tests
5. **Security Hardening**: Review security checklist in `spec.md`
6. **Deploy**: Follow deployment guides for Vercel (frontend) and Railway (backend)

---

## Reference Documentation

- **Specification**: `specs/001-auth/spec.md`
- **Data Model**: `specs/001-auth/data-model.md`
- **API Contracts**: `specs/001-auth/contracts/`
- **Implementation Plan**: `specs/001-auth/plan.md`

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs
- **Better Auth Docs**: https://better-auth.com/docs
- **Neon Docs**: https://neon.tech/docs

---

## Support

If you encounter issues:

1. Check the **Common Issues and Solutions** section above
2. Review the specification and contracts for requirements
3. Check backend logs: Look at terminal running `uvicorn`
4. Check frontend logs: Look at browser console (F12)
5. Verify environment variables are correct
6. Ensure database is accessible

For architectural questions, refer to:
- **Constitution**: `.specify/memory/constitution.md`
- **Specification**: `specs/001-auth/spec.md`
- **Planning Document**: `specs/001-auth/plan.md`
