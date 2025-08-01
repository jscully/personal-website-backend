from app.models.user import User  # SQLAlchemy model
from app.schemas.user import UserDTO


class UserMapper:
    @staticmethod
    def to_dto(entity: User) -> UserDTO:
        return UserDTO(
            uuid=entity.id,  # type: ignore
            email=entity.email,  # type: ignore
            is_active=entity.is_active,  # type: ignore
            last_login=entity.last_login,  # type: ignore
        )
