from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.models.category import Category, Subcategory
from app.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse,
    SubcategoryCreate, SubcategoryUpdate, SubcategoryResponse
)
from app.api.deps import get_current_admin
from slugify import slugify
from datetime import datetime

router = APIRouter()


# Category endpoints
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all categories (Admin only)"""
    categories = db.query(Category).all()
    return [CategoryResponse(**cat.to_dict()) for cat in categories]


@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new category (Admin only)"""
    # Check if category name already exists
    existing = db.query(Category).filter(Category.name == category_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    
    # Create category
    category = Category(
        name=category_data.name,
        slug=slugify(category_data.name),
        description=category_data.description,
        is_active=category_data.is_active
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return CategoryResponse(**category.to_dict())


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: str,
    category_data: CategoryUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update category (Admin only)"""
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Update fields
    if category_data.name is not None:
        # Check if new name already exists
        existing = db.query(Category).filter(
            Category.name == category_data.name,
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )
        category.name = category_data.name
        category.slug = slugify(category_data.name)
    
    if category_data.description is not None:
        category.description = category_data.description
    
    if category_data.is_active is not None:
        category.is_active = category_data.is_active
    
    category.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(category)
    
    return CategoryResponse(**category.to_dict())


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete category (Admin only)"""
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    db.delete(category)
    db.commit()
    
    return None


# Subcategory endpoints
@router.get("/subcategories", response_model=List[SubcategoryResponse])
def list_subcategories(
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all subcategories (Admin only)"""
    subcategories = db.query(Subcategory).all()
    return [SubcategoryResponse(**subcat.to_dict()) for subcat in subcategories]


@router.post("/subcategories", response_model=SubcategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    subcategory_data: SubcategoryCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new subcategory (Admin only)"""
    # Check if category exists
    category = db.query(Category).filter(Category.id == subcategory_data.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Create subcategory
    subcategory = Subcategory(
        category_id=subcategory_data.category_id,
        name=subcategory_data.name,
        slug=slugify(subcategory_data.name),
        description=subcategory_data.description,
        is_active=subcategory_data.is_active
    )
    
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    
    return SubcategoryResponse(**subcategory.to_dict())


@router.put("/subcategories/{subcategory_id}", response_model=SubcategoryResponse)
def update_subcategory(
    subcategory_id: str,
    subcategory_data: SubcategoryUpdate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update subcategory (Admin only)"""
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategory not found"
        )
    
    # Update fields
    if subcategory_data.name is not None:
        subcategory.name = subcategory_data.name
        subcategory.slug = slugify(subcategory_data.name)
    
    if subcategory_data.description is not None:
        subcategory.description = subcategory_data.description
    
    if subcategory_data.is_active is not None:
        subcategory.is_active = subcategory_data.is_active
    
    subcategory.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(subcategory)
    
    return SubcategoryResponse(**subcategory.to_dict())


@router.delete("/subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    subcategory_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete subcategory (Admin only)"""
    subcategory = db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
    
    if not subcategory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subcategory not found"
        )
    
    db.delete(subcategory)
    db.commit()
    
    return None
