from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token, create_refresh_token


class AuthService:
    def __init__(self, db: Session, user_repository: Optional[UserRepository] = None):
        self.db = db
        self.user_repository = user_repository or UserRepository(db)

    def authenticate_user(self, email: str, password: str):
        user = self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            return None
        if not bool(user.is_active):
            return None
        return user

    def login(self, user_id: str):
        self.user_repository.update_last_login(user_id, datetime.utcnow())
        access_token = create_access_token({"sub": str(user_id)})
        refresh_token = create_refresh_token({"sub": str(user_id)})

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 3600,
            "refresh_token": refresh_token,
        }
