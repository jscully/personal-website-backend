from typing import List, Optional, Tuple
from uuid import UUID
from sqlalchemy import and_, or_, desc, asc, func, text
from sqlalchemy.orm import Session, joinedload

from app.data.models.blog import Blog
from app.data.models.tag import Tag
from app.data.repositories.base import CRUDBase


class BlogRepository(CRUDBase[Blog, None, None]):
    """Repository for Blog entities with advanced filtering and pagination."""

    def __init__(self):
        super().__init__(Blog)

    def get_published_blogs(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10,
        tag_uuids: Optional[List[UUID]] = None,
        search_term: Optional[str] = None,
        sort_by: str = "publication_dt",
        sort_dir: str = "desc"
    ) -> Tuple[List[Blog], int]:
        """
        Get published blogs with filtering, pagination and sorting.

        Returns:
            Tuple of (blogs_list, total_count)
        """
        # Base query for published blogs
        query = db.query(Blog).options(joinedload(Blog.tags)).filter(
            Blog.status == "published"
        )

        if tag_uuids:
            query = query.join(Blog.tags).filter(Tag.id.in_(tag_uuids))

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    Blog.title.ilike(search_pattern),
                    Blog.content.ilike(search_pattern),
                    Blog.excerpt.ilike(search_pattern)
                )
            )

        total_count = query.distinct().count() if tag_uuids else query.count()

        sort_column = getattr(Blog, sort_by, Blog.publication_dt)
        if sort_dir.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))

        offset = (page - 1) * page_size
        blogs = query.distinct().offset(offset).limit(page_size).all()

        return blogs, total_count

    def get_by_slug(self, db: Session, slug: str) -> Optional[Blog]:
        """Get a blog by its slug."""
        return db.query(Blog).filter(Blog.slug == slug).first()

    def get_published_by_slug(self, db: Session, slug: str) -> Optional[Blog]:
        """Get a published blog by its slug."""
        return db.query(Blog).filter(
            and_(Blog.slug == slug, Blog.status == "published")
        ).first()