from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from uuid import UUID


class TagDTO(BaseModel):
    """Data Transfer Object for Tag in blog responses"""
    
    uuid: UUID
    name: str
    color_code: Optional[str] = None

    class Config:
        from_attributes = True


class BlogListItemDTO(BaseModel):
    """Data Transfer Object for individual blog items in list responses"""
    
    uuid: UUID
    title: str
    slug: str
    excerpt: Optional[str] = None
    publication_date: Optional[datetime] = Field(None, alias="publication_dt")
    reading_time: Optional[int] = None
    tags: List[TagDTO] = []

    class Config:
        from_attributes = True
        populate_by_name = True


class BlogListResponseDTO(BaseModel):
    """Data Transfer Object for paginated blog list response"""
    
    items: List[BlogListItemDTO]
    total: int
    page: int
    page_size: int
    total_pages: int

    class Config:
        from_attributes = True


class BlogDetailDTO(BaseModel):
    """Data Transfer Object for detailed blog response"""
    
    uuid: UUID
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    publication_date: Optional[datetime] = Field(None, alias="publication_dt")
    updated_date: datetime = Field(alias="updated_dt")
    reading_time: Optional[int] = None
    featured_image: Optional[str] = None
    seo_description: Optional[str] = None
    tags: List[TagDTO] = []

    class Config:
        from_attributes = True
        populate_by_name = True