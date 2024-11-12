from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .schemas import UserBase, UserCreate, UserLogin, UserCharacter, UserResponse
from .service import UserService
from src.core.database import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .utils import *
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_jti_to_blocklist
from src.mail import mail, create_message
from src.auth.schemas import EmailModel

REFRESH_TOKEN_EXPIRY = 7
auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user_account(user_data: UserCreate, db: Session = Depends(get_db)):
    email = user_data.email

    user_exists = user_service.user_exists(email, db)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )
    new_user = user_service.create_user(user_data, db)
    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html_message = f"""
    <h1>Verify your Email</h1>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    """

    message = create_message(
        recipients=[email], subject="Verify your email", body=html_message
    )

    await mail.send_message(message)

    return new_user 

@auth_router.get("/verify/{token}")
async def verify_user_account(token: str, session: Session = Depends(get_db)):

    token_data = decode_url_safe_token(token)

    user_email = token_data.get("email")

    if user_email:
        user = user_service.get_user_by_email(user_email, session)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not found",
            )

        user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


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


@auth_router.post("/send_mail")
async def send_mail(emails: EmailModel):
    emails = emails.addresses

    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    message = create_message(recipients=emails, subject=subject, body=html)
    await mail.send_message(message)

    return {"message": "Email sent successfully"}
