from .schemas import UserCreate
from .utils import generate_password_hash
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.db.models import Character
from src.db.models import User


class UserService:
    def get_user_by_email(self, email: str, db: Session):
        return db.query(User).filter(User.email == email).first()

    def user_exists(self, email, db: Session):
        user = self.get_user_by_email(email, db)
        return True if user is not None else False

    def create_user(self, user_data: UserCreate, db: Session):
        user_data_dict = user_data.model_dump()

        user_data_dict["password_hash"] = generate_password_hash(
            user_data_dict.pop("password")
        )

        new_user = User(**user_data_dict)

        db.add(new_user)

        db.commit()
        db.refresh(new_user)

        return new_user

    def buy_character(self, user_uid: str, character_id: int, db: Session):
        user = db.query(User).filter(User.uid == user_uid).first()
        character = db.query(Character).filter(Character.id == character_id).first()

        if not user:
            return None, "User not found"

        if not character:
            return None, "Character not found"

        if user.balance < character.new_price:
            return None, "Insufficient balance"

        user.balance -= character.new_price
        user.characters.append(character)

        try:
            db.commit()
            db.refresh(user)
            return {
                "msg": f"Character '{character.name}' purchased successfully."
            }, None
        except IntegrityError:
            db.rollback()
            return None, "Error while processing the purchase."
