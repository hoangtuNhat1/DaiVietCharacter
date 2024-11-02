from fastapi import FastAPI, UploadFile
from src.core.firebase import init_firebase
from src.core.database import init_db
from src.characters.api import router as character_router
from src.auth.api import auth_router as auth_router


def lifespan(app: FastAPI):
    init_db()
    yield
    print("server is stopping")


app = FastAPI(lifespan=lifespan)

init_firebase()
app.include_router(character_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
