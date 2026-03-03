from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, func
from typing import List
from uuid import UUID

from app.api.deps import get_db, get_current_buyer
from app.models.user import User
from app.models.quote_request import CategoryQuoteRequest, QuoteRequestFollowup
from app.models.category import Category

router = APIRouter()


@router.get("/my-quotes")
def get_buyer_quotes(
    db: Session = Depends(get_db),
    current_buyer: User = Depends(get_current_buyer)
):
    """
    Get all quote requests for the current buyer
    """
    # Get quotes for this buyer
    query = db.query(CategoryQuoteRequest).options(
        joinedload(CategoryQuoteRequest.category)
    ).filter(
        CategoryQuoteRequest.buyer_id == current_buyer.id
    )
    
    quote_requests = query.order_by(desc(CategoryQuoteRequest.created_at)).all()
    
    # Build response with additional data
    result = []
    for qr in quote_requests:
        followup_count = db.query(func.count(QuoteRequestFollowup.id)).filter(
            QuoteRequestFollowup.quote_request_id == qr.id
        ).scalar()
        
        # Get latest followup
        latest_followup = db.query(QuoteRequestFollowup).filter(
            QuoteRequestFollowup.quote_request_id == qr.id
        ).order_by(desc(QuoteRequestFollowup.created_at)).first()
        
        qr_dict = {
            "id": str(qr.id),
            "category_id": str(qr.category_id),
            "subcategory_id": str(qr.subcategory_id) if qr.subcategory_id else None,
            "name": qr.name,
            "email": qr.email,
            "phone": qr.phone,
            "status": qr.status,
            "created_at": qr.created_at.isoformat(),
            "updated_at": qr.updated_at.isoformat(),
            "category_name": qr.category.name if qr.category else None,
            "followup_count": followup_count,
            "latest_followup": {
                "text": latest_followup.followup_text,
                "created_at": latest_followup.created_at.isoformat()
            } if latest_followup else None
        }
        result.append(qr_dict)
    
    # Get statistics
    total_quotes = len(result)
    pending_quotes = len([q for q in result if q['status'] == 'pending'])
    in_process_quotes = len([q for q in result if q['status'] == 'in-process'])
    completed_quotes = len([q for q in result if q['status'] == 'complete'])
    rejected_quotes = len([q for q in result if q['status'] == 'reject'])
    
    return {
        "quotes": result,
        "statistics": {
            "total": total_quotes,
            "pending": pending_quotes,
            "in_process": in_process_quotes,
            "completed": completed_quotes,
            "rejected": rejected_quotes
        }
    }


@router.get("/my-quotes/{quote_id}")
def get_buyer_quote_details(
    quote_id: UUID,
    db: Session = Depends(get_db),
    current_buyer: User = Depends(get_current_buyer)
):
    """
    Get specific quote request details with followups for the current buyer
    """
    quote_request = db.query(CategoryQuoteRequest).options(
        joinedload(CategoryQuoteRequest.category),
        joinedload(CategoryQuoteRequest.followups).joinedload(QuoteRequestFollowup.admin)
    ).filter(
        CategoryQuoteRequest.id == quote_id,
        CategoryQuoteRequest.buyer_id == current_buyer.id
    ).first()
    
    if not quote_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quote request not found"
        )
    
    # Build followups list
    followups_data = []
    for followup in sorted(quote_request.followups, key=lambda x: x.created_at, reverse=True):
        followups_data.append({
            "id": str(followup.id),
            "followup_text": followup.followup_text,
            "status": followup.status,
            "created_at": followup.created_at.isoformat(),
            "admin_name": followup.admin.name if followup.admin else "Admin"
        })
    
    result = {
        "id": str(quote_request.id),
        "category_id": str(quote_request.category_id),
        "subcategory_id": str(quote_request.subcategory_id) if quote_request.subcategory_id else None,
        "name": quote_request.name,
        "email": quote_request.email,
        "phone": quote_request.phone,
        "status": quote_request.status,
        "created_at": quote_request.created_at.isoformat(),
        "updated_at": quote_request.updated_at.isoformat(),
        "category_name": quote_request.category.name if quote_request.category else None,
        "followups": followups_data
    }
    
    return result
