from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, func
from sqlalchemy.orm import relationship
from ..auth.models import user_character_association
from ..common.base_model import Base


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
    users = relationship(
        "User",
        secondary=user_character_association,
        back_populates="characters",
    )
