from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.category import Category, Subcategory
from app.schemas.category import CategoryResponse, SubcategoryResponse, CategoryWithSubcategories

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
def get_public_categories(db: Session = Depends(get_db)):
    """
    Get all active categories for home page (Public endpoint)
    
    - No authentication required
    - Returns only active categories with show_on_home=True
    """
    categories = db.query(Category).filter(
        Category.is_active == True,
        Category.deleted_at == None,
        Category.show_on_home == True
    ).order_by(Category.display_order, Category.name).all()
    return [CategoryResponse(**cat.to_dict()) for cat in categories]


@router.get("/categories/{category_id}", response_model=CategoryWithSubcategories)
def get_category_with_subcategories(
    category_id: str,
    db: Session = Depends(get_db)
):
    """
    Get category with its subcategories (Public endpoint)
    
    - No authentication required
    - Returns category with all active subcategories
    """
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True,
        Category.deleted_at == None
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Get active subcategories
    subcategories = db.query(Subcategory).filter(
        Subcategory.category_id == category_id,
        Subcategory.is_active == True,
        Subcategory.deleted_at == None
    ).order_by(Subcategory.display_order, Subcategory.name).all()
    
    category_dict = category.to_dict()
    category_dict['subcategories'] = [SubcategoryResponse(**sub.to_dict()) for sub in subcategories]
    
    return CategoryWithSubcategories(**category_dict)


@router.get("/categories/{category_id}/subcategories", response_model=List[SubcategoryResponse])
def get_category_subcategories(
    category_id: str,
    db: Session = Depends(get_db)
):
    """
    Get subcategories for a category (Public endpoint)
    
    - No authentication required
    - Returns only active subcategories
    """
    # Check if category exists
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True,
        Category.deleted_at == None
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    subcategories = db.query(Subcategory).filter(
        Subcategory.category_id == category_id,
        Subcategory.is_active == True,
        Subcategory.deleted_at == None
    ).order_by(Subcategory.display_order, Subcategory.name).all()
    
    return [SubcategoryResponse(**sub.to_dict()) for sub in subcategories]



@router.get("/menu-categories", response_model=List[CategoryResponse])
def get_menu_categories(db: Session = Depends(get_db)):
    """
    Get categories for menu display (Public endpoint)
    
    - No authentication required
    - Returns only active categories with show_in_menu=True
    """
    categories = db.query(Category).filter(
        Category.is_active == True,
        Category.deleted_at == None,
        Category.show_in_menu == True
    ).order_by(Category.display_order, Category.name).all()
    return [CategoryResponse(**cat.to_dict()) for cat in categories]


from app.models.quote_request import CategoryQuoteRequest
from app.schemas.quote_request import QuoteRequestCreate


@router.post("/quote-requests", status_code=status.HTTP_201_CREATED)
def submit_quote_request(
    quote_data: QuoteRequestCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a category quote request (Public endpoint)
    
    - No authentication required for guest users
    - Buyer ID is optional (for logged-in users)
    """
    # Verify category exists
    category = db.query(Category).filter(
        Category.id == quote_data.category_id,
        Category.is_active == True,
        Category.deleted_at == None
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Create quote request
    new_quote_request = CategoryQuoteRequest(
        category_id=quote_data.category_id,
        subcategory_id=quote_data.subcategory_id,
        buyer_id=quote_data.buyer_id,
        name=quote_data.name,
        email=quote_data.email,
        phone=quote_data.phone,
        status="pending"
    )
    
    db.add(new_quote_request)
    db.commit()
    db.refresh(new_quote_request)
    
    return {
        "message": "Quote request submitted successfully",
        "quote_request_id": str(new_quote_request.id)
    }
