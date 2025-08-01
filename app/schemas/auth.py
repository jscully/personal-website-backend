from typing import Optional
from pydantic import BaseModel


class TokenPayload(BaseModel):
    """Payload data contained in JWT tokens"""

    sub: str  # Subject (usually user ID)
    exp: int  # Expiration time
    iat: int  # Issued at time
    type: str  # Token type (access or refresh)


class TokenResponse(BaseModel):
    """Schema for token response returned to client"""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
