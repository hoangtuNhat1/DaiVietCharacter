import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .association import user_character_association
from ..common.base_model import Base


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

    # New role field
    role = Column(
        String(50),
        nullable=False,
        default="user",
        info={"description": "Role of the user, e.g., 'admin', 'user', or 'guest'"},
    )

    # New balance field
    balance = Column(Float, default=0.0)  # Add a balance field for the user

    # Relationship with characters (many-to-many)
    characters = relationship(
        "Character",
        secondary=user_character_association,
        back_populates="users",
    )
