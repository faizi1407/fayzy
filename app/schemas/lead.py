from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime


class LeadCreate(BaseModel):
    email: EmailStr = Field(..., description="Customer email address")


class LeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    created_at: datetime
