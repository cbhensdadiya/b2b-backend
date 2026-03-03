from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base


class SignupRecord(Base):
    """Signup record model for tracking user registrations"""
    
    __tablename__ = "signup_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    mobile = Column(String(20), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    signup_status = Column(String(50), nullable=False)  # PENDING, VERIFIED, FAILED
    verification_method = Column(String(50), nullable=True)  # OTP, EMAIL, MANUAL
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    verified_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<SignupRecord {self.email} - {self.signup_status}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "email": self.email,
            "mobile": self.mobile,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "signup_status": self.signup_status,
            "verification_method": self.verification_method,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None
        }
