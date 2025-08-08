from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db
from app.api.schemas.blog import BlogListResponseDTO, BlogListItemDTO, TagDTO
from app.domain.services.blog_service import BlogService
from app.core.rate_limiting import limiter

router = APIRouter()


def get_blog_service() -> BlogService:
    """Dependency to get blog service instance."""
    return BlogService()


@router.get("/blogs", response_model=BlogListResponseDTO)
@limiter.limit("30/minute")
async def list_published_blogs(
    request: Request,
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=50, description="Items per page"),
    tags: Optional[str] = Query(default=None, description="Comma-separated tag UUIDs"),
    search_term: Optional[str] = Query(default=None, description="Search in title/content"),
    sort_by: str = Query(default="publication_dt", description="Sort field"),
    sort_dir: str = Query(default="desc", description="Sort direction (asc/desc)"),
    db: Session = Depends(get_db),
    blog_service: BlogService = Depends(get_blog_service)
):
    """
    List published blogs with pagination and filtering.

    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 10, max: 50)
    - **tags**: Comma-separated tag UUIDs for filtering
    - **search_term**: Search in title, content, and excerpt
    - **sort_by**: Field to sort by (publication_dt, title, updated_dt, reading_time)
    - **sort_dir**: Sort direction (asc or desc)
    """
    try:
        tag_uuids = []
        if tags:   tag_uuids = [tag.strip() for tag in tags.split(",") if tag.strip()]

        result = blog_service.get_published_blogs(
            db=db,
            page=page,
            page_size=page_size,
            tag_uuids=tag_uuids if tag_uuids else None,
            search_term=search_term,
            sort_by=sort_by,
            sort_dir=sort_dir
        )

        blog_items = []
        for blog in result["items"]:
            tag_dtos = [
                TagDTO(
                    uuid=tag.id,
                    name=tag.name,
                    color_code=tag.color_code
                )
                for tag in blog.tags
            ]

            blog_dto = BlogListItemDTO(
                uuid=blog.id,
                title=blog.title,
                slug=blog.slug,
                excerpt=blog.excerpt,
                publication_date=blog.publication_dt,
                reading_time=blog.reading_time,
                tags=tag_dtos
            )
            blog_items.append(blog_dto)

        return BlogListResponseDTO(
            items=blog_items,
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )