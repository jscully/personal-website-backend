from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from math import ceil

from app.data.repositories.blog_repository import BlogRepository
from app.data.models.blog import Blog


class BlogService:
    """Service for blog-related business logic."""

    def __init__(self, blog_repository: BlogRepository = None):
        self.blog_repository = blog_repository or BlogRepository()

    def get_published_blogs(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 10,
        tag_uuids: Optional[List[str]] = None,
        search_term: Optional[str] = None,
        sort_by: str = "publication_dt",
        sort_dir: str = "desc"
    ) -> Dict[str, Any]:
        """
        Get published blogs with pagination, filtering, and sorting.

        Args:
            db: Database session
            page: Page number (1-based)
            page_size: Items per page (max 50)
            tag_uuids: List of tag UUID strings for filtering
            search_term: Search term for title/content/excerpt
            sort_by: Field to sort by
            sort_dir: Sort direction (asc/desc)

        Returns:
            Dict with items, pagination info
        """

        page = max(1, page)
        page_size = min(max(1, page_size), 50)

        tag_uuid_objects = None
        if tag_uuids:
            try:
                tag_uuid_objects = [UUID(tag_uuid) for tag_uuid in tag_uuids if tag_uuid.strip()]
            except ValueError:
                tag_uuid_objects = None

        valid_sort_fields = ["publication_dt", "title", "updated_dt", "reading_time"]
        if sort_by not in valid_sort_fields:
            sort_by = "publication_dt"

        if sort_dir.lower() not in ["asc", "desc"]:
            sort_dir = "desc"

        search_term = search_term.strip() if search_term else None
        if search_term and len(search_term) < 2:
            search_term = None

        blogs, total_count = self.blog_repository.get_published_blogs(
            db=db,
            page=page,
            page_size=page_size,
            tag_uuids=tag_uuid_objects,
            search_term=search_term,
            sort_by=sort_by,
            sort_dir=sort_dir
        )

        total_pages = ceil(total_count / page_size) if total_count > 0 else 1

        return {
            "items": blogs,
            "total": total_count,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    def get_blog_by_slug(self, db: Session, slug: str) -> Optional[Blog]:
        """Get a published blog by slug."""
        if not slug or not slug.strip():
            return None

        return self.blog_repository.get_published_by_slug(db, slug.strip())