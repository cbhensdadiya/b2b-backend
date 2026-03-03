from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Password hashing context with BCrypt cost factor 12
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using BCrypt with cost factor 12
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    
    Args:
        data: Data to encode in token (user_id, email, role)
        expires_delta: Optional custom expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT refresh token
    
    Args:
        data: Data to encode in token (user_id)
        
    Returns:
        str: Encoded JWT refresh token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        dict: Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_permissions(db, user_id):
    """
    Get all permissions for a user based on their roles
    
    Args:
        db: Database session
        user_id: User UUID
        
    Returns:
        list: List of permission slugs or ["*"] for Master Admin
    """
    from app.models import User, UserRole, RolePermission, Permission
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    
    permissions = set()
    
    # Check if user has Master Admin role
    for user_role in user.user_roles:
        if user_role.is_active and user_role.role.slug == "master-admin":
            return ["*"]  # Master Admin has all permissions
        
        if user_role.is_active and user_role.role.is_active:
            for role_perm in user_role.role.role_permissions:
                permissions.add(role_perm.permission.slug)
    
    return list(permissions)


def has_permission(db, user_id, required_permission: str) -> bool:
    """
    Check if user has a specific permission
    
    Args:
        db: Database session
        user_id: User UUID
        required_permission: Permission slug to check
        
    Returns:
        bool: True if user has permission, False otherwise
    """
    permissions = get_user_permissions(db, user_id)
    
    # Master Admin has all permissions
    if "*" in permissions:
        return True
    
    return required_permission in permissions
