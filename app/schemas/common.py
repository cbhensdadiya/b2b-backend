from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ResponseModel(BaseModel):
    """Standard API response model"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    page_size: int = 10
    
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    """Paginated response model"""
    success: bool = True
    data: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    class Config:
        from_attributes = True
