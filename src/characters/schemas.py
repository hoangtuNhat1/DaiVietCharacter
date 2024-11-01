from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CharacterBase(BaseModel):
    short_name: str = Field(..., max_length=255)
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    background_image: Optional[str] = None
    profile_image: Optional[str] = None
    original_price: Optional[float] = None
    new_price: Optional[float] = None
    percentage_discount: Optional[float] = None


class CharacterCreate(CharacterBase):
    pass


class CharacterUpdate(BaseModel):
    short_name: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    background_image: Optional[str] = None
    profile_image: Optional[str] = None
    original_price: Optional[float] = None
    new_price: Optional[float] = None
    percentage_discount: Optional[float] = None


class CharacterInDB(CharacterBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
