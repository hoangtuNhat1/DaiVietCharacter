from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .schemas import *
from .service import *
from .ai_service import chat_character
from src.db.database import get_db
from src.auth.dependencies import RoleChecker

log_service = HistoryLogsService()
log_router = APIRouter()

# Define role-based access dependencies
admin_role_checker = Depends(RoleChecker(["admin"]))
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@log_router.post(
    "/", response_model=HistoryLogResponse, dependencies=[admin_role_checker]
)
def create_log(log: HistoryLogCreate, db: Session = Depends(get_db)):
    return log_service.create_history_log(
        db=db,
        user_id=log.user_id,
        character_id=log.character_id,
        question=log.question,
        prompt=log.prompt,
        answer=log.answer,
        feedback=log.feedback,
    )


@log_router.get(
    "/{log_id}", response_model=HistoryLogResponse, dependencies=[user_role_checker]
)
def get_log(log_id: int, db: Session = Depends(get_db)):
    log = log_service.get_history_log_by_id(db=db, log_id=log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="Log/History Log not found")
    return log


@log_router.get(
    "/user/{user_id}",
    response_model=list[HistoryLogResponse],
    dependencies=[user_role_checker],
)
def get_logs_by_user(user_id: str, db: Session = Depends(get_db)):
    logs = log_service.get_history_logs_by_user(db, user_id)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this user")
    return logs


@log_router.get(
    "/character/{character_id}",
    response_model=list[HistoryLogResponse],
    dependencies=[user_role_checker],
)
def get_history_logs_by_character(character_id: int, db: Session = Depends(get_db)):
    logs = log_service.get_history_logs_by_character(db, character_id)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this character")
    return logs


@log_router.put(
    "/{log_id}", response_model=HistoryLogResponse, dependencies=[admin_role_checker]
)
def update_feedback(log_id: int, feedback: str, db: Session = Depends(get_db)):
    updated_log = log_service.update_feedback(
        db,
        log_id,
        feedback,
    )
    if updated_log is None:
        raise HTTPException(status_code=404, detail="Log/History Log not found")
    return updated_log


@log_router.delete(
    "/{log_id}", response_model=HistoryLogResponse, dependencies=[admin_role_checker]
)
def delete_log(log_id: int, db: Session = Depends(get_db)):
    deleted_log = log_service.delete_history_log(db, log_id)
    if deleted_log is None:
        raise HTTPException(status_code=404, detail="Log/History Log not found")
    return deleted_log


@log_router.get("/{character_id}", response_model=CharacterResponse)
def get_character_with_logs(character_id: int, db: Session = Depends(get_db)):
    character = log_service.get_character_with_logs(db, character_id)
    if character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return character


@log_router.post(
    "/chat",
    response_model=HistoryLogResponse,
    dependencies=[user_role_checker],
)
async def chat_with_character(chat_input: ChatInput, db: Session = Depends(get_db)):
    user_uid = chat_input.user_uid
    character_id = chat_input.character_id
    question = chat_input.question

    # Call chat_character to get the prompt and answer, or an error message
    (response, error) = chat_character(user_uid, character_id, question, db)

    # Handle any errors by raising HTTP exceptions with appropriate status codes
    if error:
        if "not found" in error:
            raise HTTPException(status_code=404, detail=error)
        elif "do not own" in error:
            raise HTTPException(status_code=403, detail=error)
        else:
            raise HTTPException(status_code=500, detail=error)

    # Create history log entry and return response
    prompt, answer = response
    return log_service.create_history_log(
        db=db,
        user_id=user_uid,
        character_id=character_id,
        question=question,
        prompt=prompt,
        answer=answer,
    )
