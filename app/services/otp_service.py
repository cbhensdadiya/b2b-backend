import random
import string
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.otp import OTP
from app.core.config import settings


class OTPService:
    """Service for OTP generation and verification"""
    
    @staticmethod
    def generate_otp(length: int = None) -> str:
        """
        Generate a random OTP
        
        Args:
            length: OTP length (default from settings)
            
        Returns:
            str: Generated OTP
        """
        if length is None:
            length = settings.OTP_LENGTH
        
        return ''.join(random.choices(string.digits, k=length))
    
    @staticmethod
    def create_otp(db: Session, mobile: str) -> str:
        """
        Create and store OTP for mobile number
        
        Args:
            db: Database session
            mobile: Mobile number
            
        Returns:
            str: Generated OTP code
        """
        # Generate OTP
        otp_code = OTPService.generate_otp()
        
        # Calculate expiry time
        expires_at = datetime.utcnow() + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Create OTP record
        otp = OTP(
            mobile=mobile,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        db.add(otp)
        db.commit()
        db.refresh(otp)
        
        return otp_code
    
    @staticmethod
    def verify_otp(db: Session, mobile: str, otp_code: str) -> bool:
        """
        Verify OTP for mobile number
        
        Args:
            db: Database session
            mobile: Mobile number
            otp_code: OTP code to verify
            
        Returns:
            bool: True if OTP is valid, False otherwise
        """
        # Find the most recent unused OTP for this mobile
        otp = db.query(OTP).filter(
            OTP.mobile == mobile,
            OTP.otp_code == otp_code,
            OTP.is_used == False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp:
            return False
        
        # Check if OTP is expired
        if otp.is_expired():
            return False
        
        # Mark OTP as used
        otp.is_used = True
        db.commit()
        
        return True
    
    @staticmethod
    def invalidate_old_otps(db: Session, mobile: str):
        """
        Mark all old OTPs for a mobile as used
        
        Args:
            db: Database session
            mobile: Mobile number
        """
        db.query(OTP).filter(
            OTP.mobile == mobile,
            OTP.is_used == False
        ).update({"is_used": True})
        db.commit()
