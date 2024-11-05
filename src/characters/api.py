import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from . import crud, schemas
from src.core.database import get_db
from src.auth.dependencies import AccessTokenBearer

router = APIRouter()
acccess_token_bearer = AccessTokenBearer()


@router.post(
    "/characters/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CharacterInDB,
)
async def create_character(
    character: schemas.CharacterCreate,
    db: Session = Depends(get_db),
    token_details=Depends(acccess_token_bearer),
):
    print(token_details)
    db_character = crud.create_character(
        db=db,
        character=character,
    )

    return db_character


@router.get("/characters/{character_id}", response_model=schemas.CharacterInDB)
def read_character(
    character_id: int,
    db: Session = Depends(get_db),
    token_details=Depends(acccess_token_bearer),
):
    db_character = crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.get("/characters/", response_model=list[schemas.CharacterInDB])
def read_characters(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token_details=Depends(acccess_token_bearer),
):
    return crud.get_characters(db=db, skip=skip, limit=limit)


@router.put("/characters/{character_id}", response_model=schemas.CharacterInDB)
def update_character(
    character_id: int,
    character: schemas.CharacterUpdate,
    db: Session = Depends(get_db),
    token_details=Depends(acccess_token_bearer),
):
    db_character = crud.update_character(
        db, character_id=character_id, character=character
    )
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character


@router.delete("/characters/{character_id}", response_model=schemas.CharacterInDB)
def delete_character(
    character_id: int,
    db: Session = Depends(get_db),
    token_details=Depends(acccess_token_bearer),
):
    db_character = crud.delete_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return db_character
