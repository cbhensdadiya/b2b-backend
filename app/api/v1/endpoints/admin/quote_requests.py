from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_admin_user
from app.models.user import User
from app.models.quote_request import CategoryQuoteRequest, QuoteRequestFollowup
from app.models.category import Category
from app.schemas.quote_request import (
    QuoteRequestResponse,
    QuoteRequestWithFollowups,
    FollowupCreate,
    FollowupResponse
)

router = APIRouter()


@router.get("/quote-requests", response_model=List[QuoteRequestResponse])
def get_all_quote_requests(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all category quote requests with filtering
    """
    query = db.query(CategoryQuoteRequest).options(
        joinedload(CategoryQuoteRequest.category),
        joinedload(CategoryQuoteRequest.buyer)
    )
    
    if status:
        query = query.filter(CategoryQuoteRequest.status == status)
    
    quote_requests = query.order_by(desc(CategoryQuoteRequest.created_at)).offset(skip).limit(limit).all()
    
    # Build response with additional data
    result = []
    for qr in quote_requests:
        followup_count = db.query(func.count(QuoteRequestFollowup.id)).filter(
            QuoteRequestFollowup.quote_request_id == qr.id
        ).scalar()
        
        qr_dict = {
            "id": qr.id,
            "category_id": qr.category_id,
            "subcategory_id": qr.subcategory_id,
            "buyer_id": qr.buyer_id,
            "name": qr.name,
            "email": qr.email,
            "phone": qr.phone,
            "status": qr.status,
            "created_at": qr.created_at,
            "updated_at": qr.updated_at,
            "category_name": qr.category.name if qr.category else None,
            "subcategory_name": None,  # TODO: Add subcategory relationship
            "buyer_name": qr.buyer.name if qr.buyer else None,
            "followup_count": followup_count
        }
        result.append(qr_dict)
    
    return result


@router.get("/quote-requests/{quote_request_id}", response_model=QuoteRequestWithFollowups)
def get_quote_request_details(
    quote_request_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get quote request details with all followups
    """
    quote_request = db.query(CategoryQuoteRequest).options(
        joinedload(CategoryQuoteRequest.category),
        joinedload(CategoryQuoteRequest.buyer),
        joinedload(CategoryQuoteRequest.followups).joinedload(QuoteRequestFollowup.admin)
    ).filter(CategoryQuoteRequest.id == quote_request_id).first()
    
    if not quote_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote request not found"
        )
    
    # Build response
    followups_data = []
    for followup in sorted(quote_request.followups, key=lambda x: x.created_at, reverse=True):
        followups_data.append({
            "id": followup.id,
            "quote_request_id": followup.quote_request_id,
            "admin_id": followup.admin_id,
            "followup_text": followup.followup_text,
            "status": followup.status,
            "created_at": followup.created_at,
            "updated_at": followup.updated_at,
            "admin_name": followup.admin.name if followup.admin else "Unknown Admin"
        })
    
    result = {
        "id": quote_request.id,
        "category_id": quote_request.category_id,
        "subcategory_id": quote_request.subcategory_id,
        "buyer_id": quote_request.buyer_id,
        "name": quote_request.name,
        "email": quote_request.email,
        "phone": quote_request.phone,
        "status": quote_request.status,
        "created_at": quote_request.created_at,
        "updated_at": quote_request.updated_at,
        "category_name": quote_request.category.name if quote_request.category else None,
        "subcategory_name": None,
        "buyer_name": quote_request.buyer.name if quote_request.buyer else None,
        "followup_count": len(followups_data),
        "followups": followups_data
    }
    
    return result


@router.post("/quote-requests/{quote_request_id}/followups", response_model=FollowupResponse)
def create_followup(
    quote_request_id: UUID,
    followup_data: FollowupCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Create a new followup for a quote request
    """
    # Check if quote request exists
    quote_request = db.query(CategoryQuoteRequest).filter(
        CategoryQuoteRequest.id == quote_request_id
    ).first()
    
    if not quote_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote request not found"
        )
    
    # Create followup
    new_followup = QuoteRequestFollowup(
        quote_request_id=quote_request_id,
        admin_id=current_admin.id,
        followup_text=followup_data.followup_text,
        status=followup_data.status
    )
    
    db.add(new_followup)
    
    # Update quote request status
    quote_request.status = followup_data.status
    
    db.commit()
    db.refresh(new_followup)
    
    # Load admin relationship
    db.refresh(new_followup, ['admin'])
    
    return {
        "id": new_followup.id,
        "quote_request_id": new_followup.quote_request_id,
        "admin_id": new_followup.admin_id,
        "followup_text": new_followup.followup_text,
        "status": new_followup.status,
        "created_at": new_followup.created_at,
        "updated_at": new_followup.updated_at,
        "admin_name": new_followup.admin.name if new_followup.admin else "Unknown Admin"
    }


@router.get("/quote-requests/{quote_request_id}/followups", response_model=List[FollowupResponse])
def get_quote_request_followups(
    quote_request_id: UUID,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """
    Get all followups for a specific quote request
    """
    followups = db.query(QuoteRequestFollowup).options(
        joinedload(QuoteRequestFollowup.admin)
    ).filter(
        QuoteRequestFollowup.quote_request_id == quote_request_id
    ).order_by(desc(QuoteRequestFollowup.created_at)).all()
    
    result = []
    for followup in followups:
        result.append({
            "id": followup.id,
            "quote_request_id": followup.quote_request_id,
            "admin_id": followup.admin_id,
            "followup_text": followup.followup_text,
            "status": followup.status,
            "created_at": followup.created_at,
            "updated_at": followup.updated_at,
            "admin_name": followup.admin.name if followup.admin else "Unknown Admin"
        })
    
    return result
