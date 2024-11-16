import os
from sqlalchemy.orm import Session
from src.db.models import User
from src.db.models import Character
from .schemas import CharacterCreate, CharacterUpdate
from src.utils.firebase import upload_file_to_firebase


class CharacterService:

    def get_character(self, character_id: int, db: Session):
        return db.query(Character).filter(Character.id == character_id).first()

    def get_all_characters(self, db: Session):
        return db.query(Character)

    def create_character(self, character: CharacterCreate, db: Session):
        db_character = Character(
            short_name=character.short_name,
            name=character.name,
            description=character.description,
            original_price=character.original_price,
            new_price=character.new_price,
            percentage_discount=character.percentage_discount,
        )

        # Upload images if provided
        if os.path.isfile(character.profile_image):
            profile_image_url = upload_file_to_firebase(
                character.profile_image,
                f"profiles/{os.path.basename(character.profile_image)}",
            )
            db_character.profile_image = profile_image_url

        if os.path.isfile(character.background_image):
            background_image_url = upload_file_to_firebase(
                character.background_image,
                f"backgrounds/{os.path.basename(character.background_image)}",
            )
            db_character.background_image = background_image_url

        db.add(db_character)
        db.commit()
        db.refresh(db_character)
        return db_character

    def update_character(
        self, character_id: int, character: CharacterUpdate, db: Session
    ):
        db_character = self.get_character(character_id, db)
        if not db_character:
            return None
        for key, value in character.dict(exclude_unset=True).items():
            setattr(db_character, key, value)
        db.commit()
        db.refresh(db_character)
        return db_character

    def delete_character(self, character_id: int, db: Session):
        db_character = self.get_character(character_id, db)
        if db_character:
            db.delete(db_character)
            db.commit()
        return db_character

    def get_user_characters(
        self, db: Session, user_uid: str, skip: int = 0, limit: int = 10
    ):
        user = db.query(User).filter(User.uid == user_uid).first()

        if not user:
            return None  # Or raise HTTPException if user not found

        # Query the Character table directly and filter by user ID with offset and limit
        return (
            db.query(Character.id)
            .join(User.characters)
            .filter(User.uid == user_uid)
            .offset(skip)
            .limit(limit)
            .all()
        )
