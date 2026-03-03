from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.api.deps import require_permission
from app.models import User, Category, Subcategory, LoginHistory, SignupRecord, AuditLog
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats(
    current_user: User = Depends(require_permission("reports.view")),
    db: Session = Depends(get_db)
):
    """
    Get dashboard statistics
    - Requires: reports.view permission
    """
    # User statistics
    total_users = db.query(User).filter(User.deleted_at == None).count()
    active_users = db.query(User).filter(User.is_active == True, User.deleted_at == None).count()
    verified_users = db.query(User).filter(User.is_verified == True, User.deleted_at == None).count()
    
    # Category statistics
    total_categories = db.query(Category).filter(Category.deleted_at == None).count()
    active_categories = db.query(Category).filter(Category.is_active == True, Category.deleted_at == None).count()
    total_subcategories = db.query(Subcategory).filter(Subcategory.deleted_at == None).count()
    
    # Login statistics (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    successful_logins = db.query(LoginHistory).filter(
        LoginHistory.login_status == "SUCCESS",
        LoginHistory.created_at >= thirty_days_ago
    ).count()
    
    failed_logins = db.query(LoginHistory).filter(
        LoginHistory.login_status == "FAILED",
        LoginHistory.created_at >= thirty_days_ago
    ).count()
    
    # Signup statistics (last 30 days)
    recent_signups = db.query(SignupRecord).filter(
        SignupRecord.created_at >= thirty_days_ago
    ).count()
    
    verified_signups = db.query(SignupRecord).filter(
        SignupRecord.signup_status == "VERIFIED",
        SignupRecord.created_at >= thirty_days_ago
    ).count()
    
    # Recent activity
    recent_audit_logs = db.query(AuditLog).order_by(
        AuditLog.created_at.desc()
    ).limit(10).all()
    
    return {
        "success": True,
        "data": {
            "users": {
                "total": total_users,
                "active": active_users,
                "verified": verified_users,
                "inactive": total_users - active_users
            },
            "categories": {
                "total": total_categories,
                "active": active_categories,
                "subcategories": total_subcategories
            },
            "logins_last_30_days": {
                "successful": successful_logins,
                "failed": failed_logins,
                "total": successful_logins + failed_logins
            },
            "signups_last_30_days": {
                "total": recent_signups,
                "verified": verified_signups,
                "pending": recent_signups - verified_signups
            },
            "recent_activity": [log.to_dict() for log in recent_audit_logs]
        }
    }


@router.get("/login-history")
def get_login_history(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(require_permission("login_history.view")),
    db: Session = Depends(get_db)
):
    """
    Get login history with pagination
    - Requires: login_history.view permission
    """
    query = db.query(LoginHistory).order_by(LoginHistory.created_at.desc())
    
    total = query.count()
    history = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [h.to_dict() for h in history],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/signup-records")
def get_signup_records(
    page: int = 1,
    page_size: int = 20,
    current_user: User = Depends(require_permission("signup_records.view")),
    db: Session = Depends(get_db)
):
    """
    Get signup records with pagination
    - Requires: signup_records.view permission
    """
    query = db.query(SignupRecord).order_by(SignupRecord.created_at.desc())
    
    total = query.count()
    records = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [r.to_dict() for r in records],
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/audit-logs")
def get_audit_logs(
    page: int = 1,
    page_size: int = 20,
    action: str = None,
    entity_type: str = None,
    current_user: User = Depends(require_permission("audit.view")),
    db: Session = Depends(get_db)
):
    """
    Get audit logs with filtering and pagination
    - Requires: audit.view permission
    """
    query = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    
    if action:
        query = query.filter(AuditLog.action == action)
    
    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    
    total = query.count()
    logs = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "success": True,
        "data": [log.to_dict() for log in logs],
        "total": total,
        "page": page,
        "page_size": page_size
    }
