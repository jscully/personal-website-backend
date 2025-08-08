from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.routers.admin import auth
from app.api.routers.public import blogs
from app.core.config import settings
from app.core.rate_limiting import limiter, rate_limit_exceeded_handler

app = FastAPI(
    title="Personal Website API",
    description="Backend API for Personal Professional Website",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/admin/auth", tags=["admin"])
app.include_router(blogs.router, prefix="/api", tags=["blogs"])

@app.get("/")
@limiter.limit("100/minute")
async def root(request: Request):
    return {"message": "Welcome to Personal Website API"}