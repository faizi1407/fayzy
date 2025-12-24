from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class LeadCreate(BaseModel):
    email: EmailStr = Field(..., description="Customer email address")


class LeadResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
