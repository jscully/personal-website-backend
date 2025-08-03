from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.api.deps import get_auth_service
from app.services.auth.auth_service import AuthService
from app.schemas.user import TokenResponse
from app.core.rate_limiting import limiter

router = APIRouter()

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/hour")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    OAuth2 compatible token login, get an access token for future requests
    Rate limited to 10 attempts per hour per IP address
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_service.login(user.id)

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("60/hour")
async def refresh_token(
    request: Request,
    refresh_request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Refresh access token using a valid refresh token"""
    try:
        new_tokens = auth_service.refresh_tokens(refresh_request.refresh_token)
        return new_tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )