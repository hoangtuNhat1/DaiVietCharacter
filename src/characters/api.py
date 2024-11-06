import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from . import crud, schemas
from src.core.database import get_db
from src.auth.dependencies import AccessTokenBearer
from .crud import CharacterService
from ..auth.dependencies import RoleChecker
from ..auth.dependencies import get_current_user

admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker(["user"])
admin_or_user_role_checker = RoleChecker(["admin", "user"])
character_service = CharacterService()
router = APIRouter()
access_token_bearer = AccessTokenBearer()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CharacterInDB,
    dependencies=[Depends(admin_role_checker)],
)
async def create_character(
    character: schemas.CharacterCreate,
    db: Session = Depends(get_db),
    token_details=Depends(access_token_bearer),
):
    db_character = character_service.create_character(character=character, db=db)
    return db_character


@router.get(
    "/{character_id}",
    response_model=schemas.CharacterInDB,
    dependencies=[Depends(admin_or_user_role_checker)],
)
def read_character(
    character_id: int,
    db: Session = Depends(get_db),
    token_details=Depends(access_token_bearer),
):
    db_character = character_service.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.get(
    "/",
    response_model=list[schemas.CharacterInDB],
    dependencies=[Depends(admin_or_user_role_checker)],
)
def read_characters(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token_details=Depends(access_token_bearer),
):
    return character_service.get_characters(db=db, skip=skip, limit=limit)


@router.put(
    "/{character_id}",
    response_model=schemas.CharacterInDB,
    dependencies=[Depends(admin_role_checker)],
)
def update_character(
    character_id: int,
    character: schemas.CharacterUpdate,
    db: Session = Depends(get_db),
    token_details=Depends(access_token_bearer),
):
    db_character = character_service.update_character(
        db, character_id=character_id, character=character
    )
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.delete(
    "/{character_id}",
    response_model=schemas.CharacterInDB,
    dependencies=[Depends(admin_role_checker)],
)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    token_details=Depends(access_token_bearer),
):
    db_character = character_service.delete_character(character_id=character_id, db=db)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.get(
    "/user/{user_uid}/characters",
    response_model=schemas.CharacterList,
    dependencies=[Depends(user_role_checker)],
)
def get_user_characters(
    user_uid: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    characters = character_service.get_user_characters(db, user_uid, skip, limit)
    if not characters:
        characters = []
    return {"characters": characters}
