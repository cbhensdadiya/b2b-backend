from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.core.database import get_db
from app.api.deps import require_permission
from app.models import User, UserRole as UserRoleModel, AuditLog
from pydantic import BaseModel
from datetime import datetime
import math

router = APIRouter()


class UserListResponse(BaseModel):
    success: bool
    data: list
    total: int
    page: int
    page_size: int
    total_pages: int


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    role: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(require_permission("users.view")),
    db: Session = Depends(get_db)
):
    """
    List all users with filtering and pagination
    - Requires: users.view permission
    """
    query = db.query(User).filter(User.deleted_at == None)
    
    # Apply filters
    if role:
        query = query.filter(User.role == role)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.mobile.ilike(f"%{search}%")
            )
        )
    
    # Get total count
    total = query.count()
    total_pages = math.ceil(total / page_size)
    
    # Get paginated results
    users = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [user.to_dict() for user in users],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/users/{user_id}")
def get_user(
    user_id: str,
    current_user: User = Depends(require_permission("users.view")),
    db: Session = Depends(get_db)
):
    """
    Get user details by ID
    - Requires: users.view permission
    """
    user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "data": user.to_dict()}


@router.patch("/users/{user_id}/activate")
def activate_user(
    user_id: str,
    current_user: User = Depends(require_permission("users.activate")),
    db: Session = Depends(get_db)
):
    """
    Activate a user account
    - Requires: users.activate permission
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="ACTIVATE",
        entity_type="User",
        entity_id=user_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "User activated successfully"}


@router.patch("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: str,
    current_user: User = Depends(require_permission("users.activate")),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user account
    - Requires: users.activate permission
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deactivating self
    if str(user.id) == str(current_user.id):
        raise HTTPException(
            status_code=400,
            detail="Cannot deactivate your own account"
        )
    
    user.is_active = False
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="DEACTIVATE",
        entity_type="User",
        entity_id=user_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "User deactivated successfully"}


@router.put("/users/{user_id}")
def update_user(
    user_id: str,
    user_data: dict,
    current_user: User = Depends(require_permission("users.edit")),
    db: Session = Depends(get_db)
):
    """
    Update user details
    - Requires: users.edit permission
    """
    user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update allowed fields
    if 'name' in user_data:
        user.name = user_data['name']
    if 'email' in user_data:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            User.email == user_data['email'],
            User.id != user_id,
            User.deleted_at == None
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = user_data['email']
    if 'mobile' in user_data:
        # Check if mobile is already taken by another user
        existing = db.query(User).filter(
            User.mobile == user_data['mobile'],
            User.id != user_id,
            User.deleted_at == None
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Mobile number already in use")
        user.mobile = user_data['mobile']
    if 'role' in user_data:
        user.role = user_data['role']
    if 'is_active' in user_data:
        user.is_active = user_data['is_active']
    if 'is_verified' in user_data:
        user.is_verified = user_data['is_verified']
    
    user.updated_by = current_user.id
    user.updated_at = datetime.utcnow()
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="UPDATE",
        entity_type="User",
        entity_id=user_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "User updated successfully", "data": user.to_dict()}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: str,
    current_user: User = Depends(require_permission("users.delete")),
    db: Session = Depends(get_db)
):
    """
    Soft delete a user
    - Requires: users.delete permission
    """
    user = db.query(User).filter(User.id == user_id, User.deleted_at == None).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting self
    if str(user.id) == str(current_user.id):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete your own account"
        )
    
    user.deleted_at = datetime.utcnow()
    user.deleted_by = current_user.id
    user.is_active = False
    db.commit()
    
    # Log action
    audit = AuditLog(
        user_id=current_user.id,
        action="DELETE",
        entity_type="User",
        entity_id=user_id
    )
    db.add(audit)
    db.commit()
    
    return {"success": True, "message": "User deleted successfully"}
