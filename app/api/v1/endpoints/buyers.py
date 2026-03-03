from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.buyer import BuyerListResponse, BuyerDetailResponse, BuyerUpdateRequest
from app.schemas.common import PaginatedResponse
from app.api.deps import get_current_admin
from datetime import datetime
import math

router = APIRouter()


@router.get("", response_model=PaginatedResponse)
def list_buyers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    List all buyers (paginated)
    
    - Requires Master Admin authentication
    - Returns paginated list of buyers
    """
    # Query buyers
    query = db.query(User).filter(
        User.role == UserRole.BUYER,
        User.deleted_at == None
    )
    
    total = query.count()
    total_pages = math.ceil(total / page_size)
    
    buyers = query.offset((page - 1) * page_size).limit(page_size).all()
    
    buyers_data = [BuyerListResponse(**buyer.to_dict()) for buyer in buyers]
    
    return PaginatedResponse(
        success=True,
        data=buyers_data,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{buyer_id}", response_model=BuyerDetailResponse)
def get_buyer(
    buyer_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get buyer details by ID
    
    - Requires Master Admin authentication
    """
    buyer = db.query(User).filter(
        User.id == buyer_id,
        User.role == UserRole.BUYER,
        User.deleted_at == None
    ).first()
    
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer not found"
        )
    
    return BuyerDetailResponse(**buyer.to_dict())


@router.put("/{buyer_id}", response_model=BuyerDetailResponse)
def update_buyer(
    buyer_id: str,
    update_data: BuyerUpdateRequest,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Update buyer information
    
    - Requires Master Admin authentication
    """
    buyer = db.query(User).filter(
        User.id == buyer_id,
        User.role == UserRole.BUYER,
        User.deleted_at == None
    ).first()
    
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer not found"
        )
    
    # Update fields
    if update_data.name is not None:
        buyer.name = update_data.name
    if update_data.email is not None:
        # Check if email already exists
        existing = db.query(User).filter(
            User.email == update_data.email,
            User.id != buyer_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        buyer.email = update_data.email
    if update_data.mobile is not None:
        # Check if mobile already exists
        existing = db.query(User).filter(
            User.mobile == update_data.mobile,
            User.id != buyer_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mobile number already in use"
            )
        buyer.mobile = update_data.mobile
    if update_data.is_active is not None:
        buyer.is_active = update_data.is_active
    
    buyer.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(buyer)
    
    return BuyerDetailResponse(**buyer.to_dict())


@router.delete("/{buyer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_buyer(
    buyer_id: str,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Soft delete buyer
    
    - Requires Master Admin authentication
    - Marks buyer as deleted (soft delete)
    """
    buyer = db.query(User).filter(
        User.id == buyer_id,
        User.role == UserRole.BUYER,
        User.deleted_at == None
    ).first()
    
    if not buyer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Buyer not found"
        )
    
    # Soft delete
    buyer.deleted_at = datetime.utcnow()
    buyer.is_active = False
    db.commit()
    
    return None
