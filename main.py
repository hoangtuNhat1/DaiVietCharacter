from fastapi import FastAPI, UploadFile
from src.core.firebase import init_firebase
from src.characters.api import router as character_router


app = FastAPI()

init_firebase()
app.include_router(character_router, prefix="/api/v1")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
