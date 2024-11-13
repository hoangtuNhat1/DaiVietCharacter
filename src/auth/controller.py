from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .schemas import UserCreate, UserLogin, UserCharacter, UserResponse
from .service import UserService
from src.db.database import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

# from .utils import *
from .utils import verify_password, create_access_token
from datetime import datetime, timedelta
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.utils.redis import add_jti_to_blocklist
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken

REFRESH_TOKEN_EXPIRY = 7
auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user_account(
    user_data: UserCreate, session: Session = Depends(get_db)
):
    email = user_data.email

    user_exists = user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_users(login_data: UserLogin, db: Session = Depends(get_db)):
    email = login_data.email
    password = login_data.password

    user = user_service.get_user_by_email(email, db)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )


@auth_router.post(
    "/buy-character/{character_id}",
    status_code=status.HTTP_200_OK,
)
async def buy_character(
    character_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),  # Get the current user from the token
):
    # Call the service to handle the purchase
    response, error = user_service.buy_character(
        user_uid=current_user.uid, character_id=character_id, db=db
    )

    if error:
        # Raise HTTPException if there's an error in the service logic
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return response


@auth_router.get("/me", response_model=UserCharacter)
async def get_current_user(user=Depends(get_current_user)):
    return user
