from sqlalchemy import Column, String, Table, ForeignKey, Integer
from sqlalchemy.ext.declarative import declarative_base
from ..common.base_model import Base

user_character_association = Table(
    "user_character",
    Base.metadata,
    Column("user_uid", String(36), ForeignKey("user_accounts.uid"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
)
