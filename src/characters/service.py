import os
from sqlalchemy.orm import Session
from src.db.models import User
from src.db.models import Character
from .schemas import CharacterCreate, CharacterUpdate
from src.utils.firebase import upload_file_to_firebase
from src.errors import CharacterNotFound, UserNotFound, InvalidFileType
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
class CharacterService:

    def get_character(self, character_id: int, db: Session):
        return db.query(Character).filter(Character.id == character_id).first()

    def get_all_characters(self, db: Session):
        return db.query(Character)

    def create_character(self, character: CharacterCreate, db: Session):
        character = Character(
            short_name=character.short_name,
            name=character.name,
            description=character.description,
            original_price=character.original_price,
            new_price=character.new_price,
            percentage_discount=character.percentage_discount,
        )
        db.add(character)
        db.commit()
        db.refresh(character)
        return character
    def update_images(self, character_id: int, pf_img: UploadFile, bg_img: UploadFile, db: Session) -> str:
        character = db.query(Character).filter(Character.id == character_id).first()
        if not character:
            raise CharacterNotFound()
        if not pf_img.content_type.startswith("image/"):
            raise InvalidFileType
        if not bg_img.content_type.startswith("image/"):
            raise InvalidFileType
        temp_files = []
        profile_image_url = None
        background_image_url = None
        try:
            with NamedTemporaryFile(delete=False, suffix=f".{pf_img.filename.split('.')[-1]}") as tmp_pf_img:
                tmp_pf_img.write(pf_img.file.read())
                temp_files.append(tmp_pf_img.name)
                pf_img_path = tmp_pf_img.name
                if os.path.isfile(pf_img_path):
                    profile_image_url = upload_file_to_firebase(
                        pf_img_path,
                        f"profiles/{os.path.basename(pf_img_path)}",
                    )
                character.profile_image = profile_image_url
            with NamedTemporaryFile(delete=False, suffix=f".{bg_img.filename.split('.')[-1]}") as tmp_bg_img:
                tmp_bg_img.write(bg_img.file.read())
                temp_files.append(tmp_bg_img.name)
                bg_img_path = tmp_bg_img.name
                if os.path.isfile(bg_img_path):
                    background_image_url = upload_file_to_firebase(
                        bg_img_path,
                        f"profiles/{os.path.basename(bg_img_path)}",
                    )
                character.background_image = background_image_url
            db.commit()
        finally:
            for file_path in temp_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
        return character

    def update_character(
        self, character_id: int, character_update: CharacterUpdate, db: Session
    ):
        character = self.get_character(character_id, db)
        character_data_dict = character_update.model_dump(exclude_unset=True)
        if not character:
            return CharacterNotFound()
        for key, value in character_data_dict.items():
            setattr(character, key, value)
        db.commit()
        db.refresh(character)
        return character

    def delete_character(self, character_id: int, db: Session):
        character = self.get_character(character_id, db)
        if character:
            db.delete(character)
            db.commit()
        return character

    def get_user_characters(
        self, db: Session, user_uid: str,
    ):
        user = db.query(User).filter(User.uid == user_uid).first()

        if not user:
            raise UserNotFound()

        return (
            db.query(Character.id)
            .join(User.characters)
            .filter(User.uid == user_uid)
            .all()
        )
