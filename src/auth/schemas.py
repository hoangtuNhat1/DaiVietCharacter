from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
import uuid
from datetime import datetime
from src.characters.schemas import CharacterOutDB


class UserBase(BaseModel):
    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4, description="Unique identifier for the user account"
    )
    username: str = Field(..., max_length=255)
    first_name: Optional[str] = Field(None, max_length=255)
    last_name: Optional[str] = Field(None, max_length=255)
    is_verified: bool = Field(default=False)
    email: EmailStr
    password_hash: str = Field(..., max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    role: str = Field(
        default="user", description="Role of the user, e.g., 'admin', 'user'"
    )
    balance: Optional[float] = Field(
        default=0.0, description="Balance of the user account"
    )

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
    role: str = Field(
        default="user", description="Role of the user, e.g., 'admin', 'user'"
    )
    balance: Optional[float] = Field(
        default=0.0, description="Balance of the user account"
    )


class UserLogin(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)


class UserCharacter(UserBase):
    characters: List[CharacterOutDB]
