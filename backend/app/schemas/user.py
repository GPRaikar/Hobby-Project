"""User schemas."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None
    pan_number: Optional[str] = None
    date_of_birth: Optional[date] = None
    financial_year_start: str = "2025-04"


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """User response schema."""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data payload."""
    user_id: Optional[str] = None
