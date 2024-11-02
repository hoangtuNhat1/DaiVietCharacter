from .models import User
from .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlalchemy.orm import Session


class UserService:
    def get_user_by_email(self, email: str, db: Session):
        return db.query(User).filter(User.email == email).first()

    def user_exists(self, email, db: Session):
        user = self.get_user_by_email(email, db)
        return True if user is not None else False

    def create_user(self, user_data: UserCreateModel, db: Session):
        user_data_dict = user_data.model_dump()

        user_data_dict["password_hash"] = generate_password_hash(
            user_data_dict.pop("password")
        )

        new_user = User(**user_data_dict)

        db.add(new_user)

        db.commit()
        db.refresh(new_user)

        return new_user
