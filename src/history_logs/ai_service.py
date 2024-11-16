# from src.AI.service import rag
from src.db.models import User, Character, HistoryLog
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


def chat_character(user_uid: str, character_id: int, question: str, db: Session):
    try:
        # Fetch user and character from the database
        user = db.query(User).filter(User.uid == user_uid).first()
        character = db.query(Character).filter(Character.id == character_id).first()

        # Check if user and character exist
        if not user:
            return None, "User not found."

        if not character:
            return None, "Character not found."

        # Check if the user owns the character
        if character not in user.characters:
            return (
                None,
                f"You do not own the character '{character.name}'. Please purchase it first.",
            )

        character_short_name = character.short_name
        character_name = character.name

        # Generate the prompt and answer using the RAG model
        prompt, answer = rag(question, character_short_name, character_name)

        return (prompt, answer), None  # No error, return the prompt and answer

    except SQLAlchemyError as e:
        db.rollback()
        return None, f"Database error: {str(e)}"

    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
