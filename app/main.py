from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.v1 import leads
from app.db.database import engine, Base

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create database tables on startup"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# Create FastAPI app
app = FastAPI(
    title="Fayzy Lead Capture API",
    description="Secure API for capturing customer leads",
    version="1.0.0",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routers
app.include_router(leads.router, prefix="/api/v1", tags=["leads"])


@app.get("/")
async def root():
    return {"message": "Fayzy Lead Capture API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
