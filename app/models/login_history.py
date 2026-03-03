from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from app.core.database import Base


class LoginHistory(Base):
    """Login history model for tracking user login attempts"""
    
    __tablename__ = "login_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)
    login_status = Column(String(50), nullable=False)  # SUCCESS, FAILED, LOCKED
    failure_reason = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<LoginHistory {self.email} - {self.login_status}>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id) if self.user_id else None,
            "email": self.email,
            "ip_address": self.ip_address,
            "user_agent": self.user_agent,
            "login_status": self.login_status,
            "failure_reason": self.failure_reason,
            "country": self.country,
            "city": self.city,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
