from fastapi import FastAPI, UploadFile
from src.utils.firebase import init_firebase
from src.db.database import init_db
from src.characters.api import router as character_router
from src.auth.controller import auth_router
from src.history_logs.api import log_router
from src.middleware import register_middleware
from src.errors import register_error_handlers

# Define API version
API_VERSION = "v1"


def lifespan(app: FastAPI):
    init_db()
    yield
    print("server is stopping")


app = FastAPI(lifespan=lifespan)
register_error_handlers(app)
register_middleware(app)
init_firebase()

app.include_router(
    character_router, prefix=f"/api/{API_VERSION}/characters", tags=["characters"]
)
app.include_router(auth_router, prefix=f"/api/{API_VERSION}/auth", tags=["auth"])
app.include_router(log_router, prefix=f"/api/{API_VERSION}/logs", tags=["logs"])
