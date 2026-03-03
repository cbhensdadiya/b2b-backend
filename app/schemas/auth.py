from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re


class SignupRequest(BaseModel):
    """Buyer signup request schema"""
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    mobile: str = Field(..., min_length=10, max_length=20)
    password: str = Field(..., min_length=6, max_length=100)
    role: str = "Buyer"  # Automatically set to Buyer
    firebase_uid: Optional[str] = Field(None, max_length=128)  # Firebase UID (optional)
    
    @validator('mobile')
    def validate_mobile(cls, v):
        """Validate mobile number format"""
        # Remove any spaces or special characters
        mobile = re.sub(r'[^\d]', '', v)
        if len(mobile) < 10:
            raise ValueError('Mobile number must be at least 10 digits')
        return mobile
    
    @validator('role')
    def validate_role(cls, v):
        """Ensure role is always Buyer"""
        return "Buyer"
    
    class Config:
        from_attributes = True


class SignupResponse(BaseModel):
    """Buyer signup response schema"""
    message: str
    buyer_id: str
    mobile: str
    
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response schema"""
    token: str
    refresh_token: str
    buyer: dict
    
    class Config:
        from_attributes = True


class OTPVerificationRequest(BaseModel):
    """OTP verification request schema"""
    mobile: str = Field(..., min_length=10, max_length=20)
    otp: str = Field(..., min_length=6, max_length=6)
    
    @validator('otp')
    def validate_otp(cls, v):
        """Validate OTP format"""
        if not v.isdigit():
            raise ValueError('OTP must contain only digits')
        return v
    
    class Config:
        from_attributes = True


class OTPVerificationResponse(BaseModel):
    """OTP verification response schema"""
    message: str
    success: bool = True
    
    class Config:
        from_attributes = True


class ResendOTPRequest(BaseModel):
    """Resend OTP request schema"""
    mobile: str = Field(..., min_length=10, max_length=20)
    
    class Config:
        from_attributes = True


class ResendOTPResponse(BaseModel):
    """Resend OTP response schema"""
    message: str
    
    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str
    
    class Config:
        from_attributes = True


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema"""
    token: str
    refresh_token: str
    
    class Config:
        from_attributes = True


class BuyerResponse(BaseModel):
    """Buyer information response schema"""
    id: str
    name: str
    email: str
    mobile: str
    role: str
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
