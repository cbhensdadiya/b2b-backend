from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class BuyerListResponse(BaseModel):
    """Buyer list item response schema"""
    id: str
    name: str
    email: str
    mobile: str
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class BuyerDetailResponse(BaseModel):
    """Buyer detail response schema"""
    id: str
    name: str
    email: str
    mobile: str
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BuyerUpdateRequest(BaseModel):
    """Buyer update request schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = Field(None, min_length=10, max_length=20)
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True


class BuyerUpdateResponse(BaseModel):
    """Buyer update response schema"""
    message: str
    buyer: BuyerDetailResponse
    
    class Config:
        from_attributes = True
