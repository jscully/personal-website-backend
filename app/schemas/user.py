from pydantic import (
    BaseModel,
    EmailStr,
)
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserDTO(BaseModel):
    """Data Transfer Object for User"""

    uuid: UUID
    email: EmailStr
    is_active: bool
    last_login: Optional[datetime] = None
