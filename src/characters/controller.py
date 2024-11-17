from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from .service import CharacterService
from src.auth.dependencies import RoleChecker, get_current_user
from .schemas import CharacterCreate, CharacterResponse, CharacterUpdate
admin_role_checker = RoleChecker(["admin"])
user_role_checker = RoleChecker(["user"])
admin_or_user_role_checker = RoleChecker(["admin", "user"])
character_service = CharacterService()
char_router = APIRouter()


@char_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CharacterResponse,
)
async def create_character(
    character: CharacterCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(admin_role_checker),
):
    db_character = character_service.create_character(character=character, db=db)
    return db_character

@char_router.put("/{character_id}/images", response_model=CharacterResponse)
async def update_images(
    character_id: int,
    pf_img: UploadFile = File(...),
    bg_img: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: bool = Depends(admin_role_checker),
    
):
    """
    Update the profile and background images for a character.
    """
    character = character_service.update_images(character_id, pf_img, bg_img, db)
    return character
@char_router.put("/{character_id}", response_model=CharacterResponse)
async def update_character_route(
    character_id: int,
    character_update: CharacterUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(admin_role_checker),
):
    """
    Update a character's details.
    """
    updated_character = character_service.update_character(character_id, character_update, db)
    return updated_character

# @char_router.get(
#     "/{character_id}",
#     response_model=schemas.CharacterInDB,
#     dependencies=[Depends(admin_or_user_role_checker)],
# )
# def read_character(
#     character_id: int,
#     db: Session = Depends(get_db),
#     token_details=Depends(access_token_bearer),
# ):
#     db_character = character_service.get_character(db, character_id=character_id)
#     if db_character is None:
#         raise HTTPException(status_code=404, detail="Character not found")
#     return db_character


# @char_router.get(
#     "/",
#     response_model=list[schemas.CharacterInDB],
#     dependencies=[Depends(admin_or_user_role_checker)],
# )
# def read_characters(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     token_details=Depends(access_token_bearer),
# ):
#     return character_service.get_characters(db=db, skip=skip, limit=limit)


# @char_router.put(
#     "/{character_id}",
#     response_model=schemas.CharacterInDB,
#     dependencies=[Depends(admin_role_checker)],
# )
# def update_character(
#     character_id: int,
#     character: schemas.CharacterUpdate,
#     db: Session = Depends(get_db),
#     token_details=Depends(access_token_bearer),
# ):
#     db_character = character_service.update_character(
#         db, character_id=character_id, character=character
#     )
#     if db_character is None:
#         raise HTTPException(status_code=404, detail="Character not found")
#     return db_character


# @char_router.delete(
#     "/{character_id}",
#     response_model=schemas.CharacterInDB,
#     dependencies=[Depends(admin_role_checker)],
# )
# def delete_character(
#     character_id: int,
#     db: Session = Depends(get_db),
#     token_details=Depends(access_token_bearer),
# ):
#     db_character = character_service.delete_character(character_id=character_id, db=db)
#     if db_character is None:
#         raise HTTPException(status_code=404, detail="Character not found")
#     return db_character


# @char_router.get(
#     "/user/{user_uid}/characters",
#     response_model=schemas.CharacterList,
#     dependencies=[Depends(user_role_checker)],
# )
# def get_user_characters(
#     user_uid: str, db: Session = Depends(get_db), skip: int = 0, limit: int = 10
# ):
#     characters = character_service.get_user_characters(db, user_uid, skip, limit)
#     if not characters:
#         characters = []
#     return {"characters": characters}
