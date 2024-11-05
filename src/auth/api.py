from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.core.database import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .utils import *
from .dependencies import RefreshTokenBearer, AccessTokenBearer
from src.db.redis import add_jti_to_blocklist

REFRESH_TOKEN_EXPIRY = 7
auth_router = APIRouter()
user_service = UserService()


async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    db: Session = Depends(get_db),
):
    user_email = token_details["user"]["email"]

    user = user_service.get_user_by_email(user_email, db)

    return user


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


@auth_router.post("/login")
async def login_users(login_data: UserLoginModel, db: Session = Depends(get_db)):
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

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


@auth_router.get("/logout")
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details["jti"]

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged Out Successfully"}, status_code=status.HTTP_200_OK
    )


# @auth_router.get("/me", response_model=UserBooksModel)
# async def get_current_user(user=Depends(get_current_user)):
#     return user
