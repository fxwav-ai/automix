import os
import uuid
from fastapi import UploadFile

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def save_file(file: UploadFile):
    # Generate unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, unique_name)

    # Save file
    with open(path, "wb") as buffer:
        buffer.write(await file.read())

    return path