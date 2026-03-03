from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CategoryCreate(BaseModel):
    """Category creation request schema"""
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    """Category update request schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    """Category response schema"""
    id: str
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    image_url: Optional[str]
    display_order: int
    is_active: bool
    show_on_home: bool
    show_in_menu: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SubcategoryCreate(BaseModel):
    """Subcategory creation request schema"""
    category_id: str
    name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: bool = True
    
    class Config:
        from_attributes = True


class SubcategoryUpdate(BaseModel):
    """Subcategory update request schema"""
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    is_active: Optional[bool] = None
    
    class Config:
        from_attributes = True


class SubcategoryResponse(BaseModel):
    """Subcategory response schema"""
    id: str
    category_id: str
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    display_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CategoryWithSubcategories(BaseModel):
    """Category with subcategories response schema"""
    id: str
    name: str
    slug: str
    description: Optional[str]
    icon: Optional[str]
    image_url: Optional[str]
    display_order: int
    is_active: bool
    show_on_home: bool
    show_in_menu: bool
    subcategories: List[SubcategoryResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
