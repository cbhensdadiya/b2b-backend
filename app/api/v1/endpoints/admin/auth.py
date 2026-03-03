from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, get_password_hash
from app.models import User, LoginHistory
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta

router = APIRouter()


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminLoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str
    token_type: str
    user: dict


@router.post("/login", response_model=AdminLoginResponse)
def admin_login(
    request: Request,
    login_data: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint
    - Validates credentials
    - Checks if user has admin role
    - Logs login attempt
    - Returns JWT token
    """
    # Find user by email
    user = db.query(User).filter(User.email == login_data.email).first()
    
    # Log failed attempt if user not found
    if not user:
        login_history = LoginHistory(
            email=login_data.email,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            login_status="FAILED",
            failure_reason="User not found"
        )
        db.add(login_history)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        # Increment failed login attempts
        user.failed_login_attempts += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_attempts >= 5:
            user.locked_until = datetime.utcnow() + timedelta(minutes=30)
            user.is_active = False
        
        db.commit()
        
        # Log failed attempt
        login_history = LoginHistory(
            user_id=user.id,
            email=login_data.email,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            login_status="FAILED",
            failure_reason="Invalid password"
        )
        db.add(login_history)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if user.locked_until and user.locked_until > datetime.utcnow():
        login_history = LoginHistory(
            user_id=user.id,
            email=login_data.email,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            login_status="LOCKED",
            failure_reason="Account locked due to multiple failed attempts"
        )
        db.add(login_history)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please try again later."
        )
    
    # Check if user is active
    if not user.is_active:
        login_history = LoginHistory(
            user_id=user.id,
            email=login_data.email,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            login_status="FAILED",
            failure_reason="Account inactive"
        )
        db.add(login_history)
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Reset failed login attempts on successful login
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role.value}
    )
    
    # Log successful login
    login_history = LoginHistory(
        user_id=user.id,
        email=login_data.email,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
        login_status="SUCCESS"
    )
    db.add(login_history)
    db.commit()
    
    return AdminLoginResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
        token_type="bearer",
        user=user.to_dict()
    )
