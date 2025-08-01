# backend/app/models/contact.py
from datetime import datetime  # Add this import
from sqlalchemy import Column, String, Text, DateTime, CheckConstraint

from app.models.base import Base, BaseModel

# rest of the file remains the same


class Contact(Base, BaseModel):
    """Model representing a contact form submission."""

    __tablename__ = "contact"

    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    submission_dt = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    ip_address = Column(String(45))
    status = Column(String(20), nullable=False, default="new", index=True)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "status IN ('new', 'read', 'replied', 'archived')", name="status_check"
        ),
    )
