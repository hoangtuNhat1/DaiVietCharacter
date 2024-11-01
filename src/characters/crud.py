import os
from sqlalchemy.orm import Session
from .models import Character
from .schemas import CharacterCreate, CharacterUpdate
from src.core.firebase import upload_file_to_firebase


def get_character(db: Session, character_id: int):
    return db.query(Character).filter(Character.id == character_id).first()


def get_characters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Character).offset(skip).limit(limit).all()


def create_character(
    db: Session,
    character: CharacterCreate,
):
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


def update_character(db: Session, character_id: int, character: CharacterUpdate):
    db_character = get_character(db, character_id)
    if not db_character:
        return None
    for key, value in character.dict(exclude_unset=True).items():
        setattr(db_character, key, value)
    db.commit()
    db.refresh(db_character)
    return db_character


def delete_character(db: Session, character_id: int):
    db_character = get_character(db, character_id)
    if db_character:
        db.delete(db_character)
        db.commit()
    return db_character
