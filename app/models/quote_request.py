from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class CategoryQuoteRequest(Base):
    __tablename__ = "category_quote_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), nullable=True)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    category = relationship("Category", backref="quote_requests")
    buyer = relationship("User", foreign_keys=[buyer_id], backref="quote_requests")
    followups = relationship("QuoteRequestFollowup", back_populates="quote_request", cascade="all, delete-orphan")


class QuoteRequestFollowup(Base):
    __tablename__ = "quote_request_followups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quote_request_id = Column(UUID(as_uuid=True), ForeignKey("category_quote_requests.id", ondelete="CASCADE"), nullable=False)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    followup_text = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    quote_request = relationship("CategoryQuoteRequest", back_populates="followups")
    admin = relationship("User", foreign_keys=[admin_id], backref="followups")
