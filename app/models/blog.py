# backend/app/models/blog.py
from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    CheckConstraint,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base, BaseModel

blog_tag = Table(
    "blog_tag",
    Base.metadata,
    Column(
        "blog_id", UUID, ForeignKey("blog.id", ondelete="CASCADE"), primary_key=True
    ),
    Column("tag_id", UUID, ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

related_blog = Table(
    "related_blog",
    Base.metadata,
    Column(
        "source_blog_id",
        UUID,
        ForeignKey("blog.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "related_blog_id",
        UUID,
        ForeignKey("blog.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("relationship_type", String(50)),
    CheckConstraint("source_blog_id != related_blog_id", name="different_blogs"),
)


class Blog(Base, BaseModel):
    """Model representing a blog post."""

    __tablename__ = "blog"

    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=False)
    excerpt = Column(Text)
    publication_dt = Column(DateTime)
    updated_dt = Column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    status = Column(String(20), nullable=False, default="draft", index=True)
    featured_image = Column(String(255))
    seo_description = Column(String(255))
    reading_time = Column(Integer)

    tags = relationship("Tag", secondary=blog_tag, back_populates="blogs")

    # Fixed relationship - use string references to avoid circular import issues
    related_from = relationship(
        "Blog",
        secondary=related_blog,
        primaryjoin="Blog.id == related_blog.c.source_blog_id",
        secondaryjoin="Blog.id == related_blog.c.related_blog_id",
        back_populates="related_to"
    )

    related_to = relationship(
        "Blog",
        secondary=related_blog,
        primaryjoin="Blog.id == related_blog.c.related_blog_id",
        secondaryjoin="Blog.id == related_blog.c.source_blog_id",
        back_populates="related_from"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'published', 'archived')", name="status_check"
        ),
    )