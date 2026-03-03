from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# Quote Request Schemas
class QuoteRequestCreate(BaseModel):
    category_id: UUID
    subcategory_id: Optional[UUID] = None
    buyer_id: Optional[UUID] = None
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    phone: str = Field(..., pattern=r"^[0-9]{10}$")


class QuoteRequestUpdate(BaseModel):
    status: Optional[str] = None


class QuoteRequestResponse(BaseModel):
    id: UUID
    category_id: UUID
    subcategory_id: Optional[UUID]
    buyer_id: Optional[UUID]
    name: str
    email: str
    phone: str
    status: str
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None
    subcategory_name: Optional[str] = None
    buyer_name: Optional[str] = None
    followup_count: int = 0

    class Config:
        from_attributes = True


# Followup Schemas
class FollowupCreate(BaseModel):
    followup_text: str = Field(..., min_length=1)
    status: str = Field(..., pattern=r"^(in-process|complete|reject)$")


class FollowupResponse(BaseModel):
    id: UUID
    quote_request_id: UUID
    admin_id: Optional[UUID]
    followup_text: str
    status: str
    created_at: datetime
    updated_at: datetime
    admin_name: Optional[str] = None

    class Config:
        from_attributes = True


class QuoteRequestWithFollowups(QuoteRequestResponse):
    followups: List[FollowupResponse] = []

    class Config:
        from_attributes = True
