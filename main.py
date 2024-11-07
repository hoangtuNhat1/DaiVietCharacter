from fastapi import FastAPI, UploadFile
from src.core.firebase import init_firebase
from src.core.database import init_db
from src.characters.api import router as character_router
from src.auth.api import auth_router
from src.history_logs.api import log_router

# Define API version
API_VERSION = "v1"


def lifespan(app: FastAPI):
    init_db()
    yield
    print("server is stopping")


# Initialize FastAPI application with lifespan
app = FastAPI(lifespan=lifespan)

# Initialize Firebase on app startup
init_firebase()

# Include routers with versioned prefixes and tags
app.include_router(
    character_router, prefix=f"/api/{API_VERSION}/characters", tags=["characters"]
)
app.include_router(auth_router, prefix=f"/api/{API_VERSION}/auth", tags=["auth"])
app.include_router(log_router, prefix=f"/api/{API_VERSION}/logs", tags=["logs"])
