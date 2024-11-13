from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import uuid
from datetime import datetime
from src.characters.schemas import CharacterOutDB


class UserBase(BaseModel):
    """
    UserBase cung cấp các thuộc tính cơ bản của tài khoản người dùng,
    bao gồm thông tin nhận dạng và các chi tiết tài khoản.
    """

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Unique identifier for the user account"
    )
    username: str = Field(..., max_length=255, description="Username of the user")
    first_name: Optional[str] = Field(
        None, max_length=255, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, max_length=255, description="Last name of the user"
    )
    email: EmailStr = Field(..., description="User's email address")
    password_hash: str = Field(
        ..., max_length=255, description="Hashed password of the user"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of account creation"
    )
    role: str = Field(
        default="user", description="Role of the user, e.g., 'admin', 'user'"
    )
    balance: Optional[float] = Field(
        default=0.0, description="Balance of the user account"
    )

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    """
    UserCreate là lược đồ dùng để tạo tài khoản người dùng mới.
    """

    first_name: str = Field(..., max_length=25, description="First name of the user")
    last_name: str = Field(..., max_length=25, description="Last name of the user")
    username: str = Field(..., max_length=8, description="Username of the user")
    email: EmailStr = Field(..., max_length=40, description="User's email address")
    password: str = Field(
        ..., min_length=6, description="Password for the user account"
    )
    # role: str = Field(
    #     default="user", description="Role of the user, e.g., 'admin', 'user'"
    # )
    # balance: Optional[float] = Field(
    #     default=0.0, description="Balance of the user account"
    # )


class UserLogin(BaseModel):
    """
    UserLogin chứa thông tin đăng nhập của người dùng.
    """

    email: EmailStr = Field(..., max_length=40, description="User's email address")
    password: str = Field(
        ..., min_length=6, description="Password for the user account"
    )


class UserCharacter(UserBase):
    """
    UserCharacter kế thừa từ UserBase và bổ sung danh sách các nhân vật liên quan đến người dùng.
    """

    characters: List[CharacterOutDB] = Field(
        ..., description="List of characters associated with the user"
    )


class UserUpdate(BaseModel):
    """
    UserUpdate là lược đồ để cập nhật thông tin người dùng.
    """

    first_name: Optional[str] = Field(
        None, max_length=255, description="First name of the user"
    )
    last_name: Optional[str] = Field(
        None, max_length=255, description="Last name of the user"
    )
    username: Optional[str] = Field(
        None, max_length=255, description="Username of the user"
    )
    email: Optional[EmailStr] = Field(
        None, max_length=255, description="User's email address"
    )
    password: Optional[str] = Field(
        None, min_length=6, description="Password for the user account"
    )
    # balance: Optional[float] = Field(None, description="Balance of the user account")

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    """
    UserResponse chứa các thông tin trả về về người dùng khi thực hiện các thao tác truy vấn.
    """

    uid: uuid.UUID = Field(..., description="Unique identifier for the user account")
    username: str = Field(..., description="Username of the user")
    email: EmailStr = Field(..., description="User's email address")
    first_name: Optional[str] = Field(None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    role: str = Field(..., description="Role of the user, e.g., 'admin', 'user'")
    balance: float = Field(..., description="Balance of the user account")

    class Config:
        orm_mode = True
