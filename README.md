# Fayzy - Lead Capture API

A secure FastAPI application for capturing and validating customer email leads.

## Features

- ✅ Email validation using Pydantic v2
- ✅ PostgreSQL database with SQLAlchemy and asyncpg
- ✅ Rate limiting (5 requests per minute per IP)
- ✅ Duplicate email detection
- ✅ Performance optimized (database inserts < 50ms)
- ✅ Comprehensive error handling

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

## Database Setup

```bash
# Create PostgreSQL database
createdb fayzy

# The application will automatically create tables on startup
```

## Running the Application

```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoints

### POST /api/v1/leads

Create a new lead with email validation.

**Request:**
```json
{
  "email": "customer@example.com"
}
```

**Responses:**
- `201 Created` - Lead successfully created
- `409 Conflict` - Email already exists
- `422 Unprocessable Entity` - Invalid email format
- `429 Too Many Requests` - Rate limit exceeded (5 per minute per IP)

## Running Tests

```bash
# Create test database
createdb fayzy_test

# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Environment Variables

Create a `.env` file:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/fayzy
RATE_LIMIT=5/minute
```

## Technical Stack

- **FastAPI** - Modern web framework
- **Pydantic v2** - Data validation
- **SQLAlchemy** - ORM with async support
- **asyncpg** - PostgreSQL async driver
- **SlowAPI** - Rate limiting middleware
- **pytest** - Testing framework
