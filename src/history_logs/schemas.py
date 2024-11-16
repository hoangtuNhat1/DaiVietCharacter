from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
from src.characters.schemas import CharacterOutDB


class Feedback(str, Enum):
    like = "like"
    dislike = "dislike"


# Request schema (for creating new history logs)
class HistoryLogCreate(BaseModel):
    user_id: str
    character_id: int
    question: str
    prompt: str
    answer: str
    feedback: Optional[Feedback] = None

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dictionary


# Response schema (for sending history log data)
class HistoryLogResponse(BaseModel):
    id: int
    user_id: str
    character_id: int
    question: str
    prompt: str
    answer: str
    feedback: Optional[Feedback]
    created_at: datetime

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dictionary


class CharacterResponse(CharacterOutDB):
    history_logs: List[HistoryLogResponse]  # List of history logs for this character

    class Config:
        orm_mode = True


class ChatInput(BaseModel):

    user_uid: str
    character_id: int
    question: str

    class Config:
        orm_mode = True  # Tells Pydantic to treat the SQLAlchemy model as a dictionary
