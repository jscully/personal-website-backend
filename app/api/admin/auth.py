from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.api.deps import get_auth_service
from app.services.auth.auth_service import AuthService
from app.schemas.user import TokenResponse
from app.core.rate_limiting import limiter

router = APIRouter()

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