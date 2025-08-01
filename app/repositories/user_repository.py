from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def update_last_login(self, user_id: str, timestamp):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            setattr(user, "last_login", timestamp)
            self.db.commit()
