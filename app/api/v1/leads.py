from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import logging

from app.schemas.lead import LeadCreate, LeadResponse
from app.models.lead import Lead
from app.db.database import get_db

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
logger = logging.getLogger(__name__)


@router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_lead(
    request: Request,
    lead: LeadCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new lead with email validation.
    
    - **email**: Valid email address (required)
    
    Returns:
    - **201 Created**: Lead successfully created
    - **409 Conflict**: Email already exists
    - **422 Unprocessable Entity**: Invalid email format
    - **429 Too Many Requests**: Rate limit exceeded (5 per minute per IP)
    """
    # Record start time for performance monitoring
    start_time = time.time()
    
    try:
        # Create new lead
        db_lead = Lead(email=lead.email)
        db.add(db_lead)
        await db.commit()
        await db.refresh(db_lead)
        
        # Check performance requirement
        elapsed_time = (time.time() - start_time) * 1000  # Convert to ms
        if elapsed_time >= 50:
            logger.warning(f"Database insert took {elapsed_time:.2f}ms (>50ms threshold)")
        
        return db_lead
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )
