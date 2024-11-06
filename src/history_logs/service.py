from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from src.db.models import HistoryLog
from src.db.models import Character


class HistoryLogsService:

    def create_history_log(
        self,
        db: Session,
        user_id: int,
        character_id: int,
        question: str,
        prompt: str,
        answer: str,
        feedback: str = None,
    ) -> HistoryLog:
        try:
            history_log = HistoryLog(
                user_id=user_id,
                character_id=character_id,  # Changed from agent_id to character_id
                question=question,
                prompt=prompt,
                answer=answer,
                feedback=feedback,
                created_at=datetime.now(),
            )
            db.add(history_log)
            db.commit()
            return history_log
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error while creating history log: {str(e)}")

    def get_history_log_by_id(self, db: Session, log_id: int) -> list:
        try:
            return db.query(HistoryLog).filter_by(id=log_id).all()
        except SQLAlchemyError as e:
            raise Exception(
                f"Error while fetching history logs for user {log_id}: {str(e)}"
            )

    def get_history_logs_by_user(self, db: Session, user_id: str) -> list:
        try:
            return db.query(HistoryLog).filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            raise Exception(
                f"Error while fetching history logs for user {user_id}: {str(e)}"
            )

    def get_history_logs_by_character(self, db: Session, character_id: int) -> list:
        try:
            return (
                db.query(HistoryLog).filter_by(character_id=character_id).all()
            )  # Changed from agent_id to character_id
        except SQLAlchemyError as e:
            raise Exception(
                f"Error while fetching history logs for character {character_id}: {str(e)}"
            )

    def get_feedback_for_log(self, db: Session, log_id: int) -> str:
        try:
            history_log = db.query(HistoryLog).filter_by(id=log_id).first()
            if history_log:
                return history_log.feedback
            else:
                return None
        except SQLAlchemyError as e:
            raise Exception(f"Error while fetching feedback for log {log_id}: {str(e)}")

    def update_feedback(self, db: Session, log_id: int, feedback: str) -> bool:
        try:
            history_log = db.query(HistoryLog).filter_by(id=log_id).first()
            if history_log:
                history_log.feedback = feedback
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error while updating feedback for log {log_id}: {str(e)}")

    def delete_history_log(self, db: Session, log_id: int) -> bool:
        try:
            history_log = db.query(HistoryLog).filter_by(id=log_id).first()
            if history_log:
                db.delete(history_log)
                db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.rollback()
            raise Exception(f"Error while deleting history log {log_id}: {str(e)}")

    def get_character_with_logs(self, db: Session, character_id: int) -> bool:
        character = (
            db.query(Character)
            .options(joinedload(Character.history_logs))  # Eager load history logs
            .filter(Character.id == character_id)
            .first()
        )
        return character
