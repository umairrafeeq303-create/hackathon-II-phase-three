# Backend Agent Skills

## 1. FastAPI Framework
- App initialization and configuration
- Route decorators (@app.get, @app.post, etc.)
- Path parameters and query parameters
- Request body parsing
- Response models
- Status codes
- Dependencies (Depends)
- Middleware setup
- CORS configuration
- Startup and shutdown events

## 2. SQLModel ORM
- Model definition with table=True
- Field types and constraints
- Primary keys and foreign keys
- Relationships
- Indexes
- Optional fields
- Default values
- Timestamps
- Query operations (select, filter, join)
- Async session handling

## 3. Database Management
- PostgreSQL connection with Neon DB
- create_engine configuration
- Session management
- Connection pooling
- Table creation
- Transaction handling
- Error handling
- Migration basics

## 4. Authentication & Security
- JWT token generation (python-jose)
- Token encoding and decoding
- Token expiry handling
- OAuth2PasswordBearer
- Password hashing (passlib + bcrypt)
- Password verification
- Protected route dependencies
- User session management

## 5. Pydantic Models
- BaseModel for schemas
- Field validation
- Email validation
- Custom validators
- Response models
- Nested models
- Optional fields
- Default values

## 6. API Design
- RESTful conventions
- Endpoint naming
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Request/Response structure
- Error responses
- Status codes (200, 201, 400, 401, 403, 404, 422, 500)
- API versioning basics

## 7. Error Handling
- HTTPException usage
- Custom exception handlers
- Validation errors
- Database errors
- Try-catch blocks
- Error logging
- User-friendly messages

## 8. Environment Configuration
- python-dotenv
- Environment variables
- .env file structure
- Secret management
- Configuration validation

## 9. Railway Deployment
- Railway CLI basics
- Environment variable setup
- Database connection strings
- Port configuration
- Health check endpoints
- Deployment logs
- Domain setup

## 10. Testing & Documentation
- Swagger UI (automatic)
- OpenAPI schema
- Endpoint testing
- Manual testing with curl/Postman
- Request/Response examples