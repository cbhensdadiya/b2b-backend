from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        credentials: HTTP Bearer token
        db: Database session
        
    Returns:
        User: Current user
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    payload = decode_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def get_current_buyer(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current buyer user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current buyer
        
    Raises:
        HTTPException: If user is not a buyer
    """
    if current_user.role != UserRole.BUYER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Buyer access required."
        )
    
    return current_user


def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User: Current admin
        
    Raises:
        HTTPException: If user is not an admin
    """
    if current_user.role != UserRole.MASTER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized. Admin access required."
        )
    
    return current_user


def require_permission(permission: str):
    """
    Dependency factory to check if user has required permission
    
    Args:
        permission: Permission slug required (e.g., "users.view")
        
    Returns:
        Callable: Dependency function that checks permission
        
    Usage:
        @router.get("/users")
        def list_users(
            current_user: User = Depends(require_permission("users.view")),
            db: Session = Depends(get_db)
        ):
            ...
    """
    def permission_checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        from app.core.security import has_permission
        
        if not has_permission(db, current_user.id, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied. Required permission: {permission}"
            )
        
        return current_user
    
    return permission_checker


# Alias for backward compatibility
get_current_admin_user = get_current_admin
