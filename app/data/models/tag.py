# backend/app/models/tag.py
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from app.data.models.base import Base, BaseModel
from app.data.models.blog import blog_tag


class Tag(Base, BaseModel):
    """Model representing a content tag."""

    __tablename__ = "tag"

    name = Column(String(50), nullable=False, unique=True, index=True)
    description = Column(Text)
    color_code = Column(String(7))

    # Relationships
    blogs = relationship("Blog", secondary=blog_tag, back_populates="tags")
