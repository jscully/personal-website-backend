from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.admin import auth
from app.core.config import settings

app = FastAPI(
    title="Personal Website API",
    description="Backend API for Personal Professional Website",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(settings.CORS_ORIGINS)

app.include_router(auth.router, prefix="/api/admin/auth", tags=["admin"])


@app.get("/")
async def root():
    return {"message": "Welcome to Personal Website API"}
