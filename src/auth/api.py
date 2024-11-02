from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel
from .service import UserService
from src.core.database import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

auth_router = APIRouter()
user_service = UserService()


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreateModel, db: Session = Depends(get_db)
):
    email = user_data.email

    user_exists = user_service.user_exists(email, db)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )
    new_user = user_service.create_user(user_data, db)

    return new_user
