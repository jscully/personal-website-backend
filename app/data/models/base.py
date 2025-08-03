import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    """Base model class that includes common fields and methods."""
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    created_dt = Column(DateTime, nullable=False, default=datetime.utcnow)