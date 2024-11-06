import uuid
from sqlalchemy import (
    Column,
    String,
    Boolean,
    TIMESTAMP,
    func,
    Float,
    Enum,
    Text,
    Table,
    ForeignKey,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

user_character_association = Table(
    "user_character",
    Base.metadata,
    Column("user_uid", String(36), ForeignKey("user_accounts.uid"), primary_key=True),
    Column("character_id", Integer, ForeignKey("characters.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user_accounts"

    uid = Column(
        String(36),
        primary_key=True,
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
    )
    username = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    is_verified = Column(Boolean, default=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Role and balance fields
    role = Column(
        String(50),
        nullable=False,
        default="user",
        info={"description": "Role of the user, e.g., 'admin', 'user', or 'guest'"},
    )
    balance = Column(Float, default=0.0)

    # Relationship with characters (many-to-many)
    characters = relationship(
        "Character",
        secondary=user_character_association,
        back_populates="users",
    )

    # Relationship with history logs (one-to-many)
    history_logs = relationship("HistoryLog", back_populates="user")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_name = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    background_image = Column(Text, nullable=True)
    profile_image = Column(Text, nullable=True)
    original_price = Column(Float, nullable=True)
    new_price = Column(Float, nullable=True)
    percentage_discount = Column(Float, nullable=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )

    # Relationship with users (many-to-many)
    users = relationship(
        "User",
        secondary=user_character_association,
        back_populates="characters",
    )

    # Relationship with history logs (one-to-many)
    history_logs = relationship("HistoryLog", back_populates="character")


class HistoryLog(Base):
    __tablename__ = "history_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("user_accounts.uid"), nullable=False)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    question = Column(Text, nullable=False)
    prompt = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    feedback = Column(Enum("like", "dislike", name="feedback_enum"), nullable=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )

    # Define relationships with unique back_populates
    user = relationship("User", back_populates="history_logs")
    character = relationship("Character", back_populates="history_logs")
