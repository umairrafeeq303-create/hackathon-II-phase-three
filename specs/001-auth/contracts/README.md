# API Contracts: Authentication & User Management System

**Feature**: 001-auth
**Date**: 2026-01-09
**Phase**: 1 (Design)

## Overview

This directory contains the API contract definitions for the Authentication & User Management System. These contracts serve as the formal specification for communication between the Next.js frontend and FastAPI backend.

## Contract Structure

Each endpoint has its own contract file defining:
- Request schema (method, path, headers, body)
- Response schema (status codes, body structure)
- Error responses (all possible error cases)
- Validation rules
- Examples

## Contract Files

1. **`signup.contract.md`** - User registration endpoint
2. **`signin.contract.md`** - User authentication endpoint
3. **`me.contract.md`** - Get current user information endpoint

## Usage

### Backend Implementation

FastAPI route handlers MUST:
- Accept request bodies matching the request schema exactly
- Return responses matching the response schema exactly
- Return appropriate HTTP status codes as documented
- Include all error responses as specified

### Frontend Implementation

Next.js API client MUST:
- Send requests matching the request schema exactly
- Handle all documented response status codes
- Parse response bodies according to response schema
- Display appropriate error messages for each error case

## Validation Rules

All contracts enforce:
- Type safety (string, number, boolean, UUID)
- Length constraints (min/max length for strings)
- Format validation (email format, UUID format)
- Required vs optional fields
- Enum values (where applicable)

## HTTP Status Codes

### Success Codes
- **200 OK**: Successful GET, PUT, DELETE operations
- **201 Created**: Successful POST operations (resource created)

### Client Error Codes
- **400 Bad Request**: Invalid input format or business rule violation
- **401 Unauthorized**: Missing, invalid, or expired authentication token
- **403 Forbidden**: Valid authentication but insufficient permissions
- **404 Not Found**: Requested resource does not exist
- **422 Unprocessable Entity**: Request validation failed

### Server Error Codes
- **500 Internal Server Error**: Unexpected server error

## Security Considerations

### Authentication Headers

Protected endpoints require:
```
Authorization: Bearer <jwt_token>
```

### CORS Configuration

Backend MUST:
- Allow requests only from configured frontend origin
- Allow credentials (Authorization header)
- Allow methods: GET, POST, PUT, DELETE, OPTIONS
- Allow headers: Content-Type, Authorization

### Sensitive Data

Contracts explicitly exclude:
- Password hashes (never returned in responses)
- Internal error details (generic 500 messages)
- Stack traces (not exposed to clients)

## Contract Versioning

Current version: **v1.0**

Changes to contracts require:
1. Version increment in contract files
2. Migration guide if breaking changes
3. Backward compatibility period (if applicable)
4. Documentation of all changes

## Testing

Each contract includes:
- Request examples (valid cases)
- Response examples (success cases)
- Error examples (all error cases)

These examples MUST be used for:
- Unit tests (backend route handlers)
- Integration tests (frontend-backend communication)
- API documentation (Swagger/OpenAPI)
