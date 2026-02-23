from fastapi import APIRouter, UploadFile, File
from app.services.storage import save_file
from app.services.jobs import create_job, get_job
from fastapi.responses import FileResponse
from app.services.analysis import analyze_track

import uuid

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    return {"test": "endpoint works"}

# @router.post("/analyze")
#async def analyze(file: UploadFile = File(...)):
  #  path = await save_file(file)

 #   result = analyze_track(path)

#    return result 

@router.post("/upload")
async def upload_tracks(files: list[UploadFile] = File(...)):
    paths = []
    for file in files:
        path = await save_file(file)
        paths.append(path)

    job_id = create_job(paths)
    return {"job_id": job_id}

@router.get("/status/{job_id}")
def job_status(job_id: str):
    return get_job(job_id)

@router.get("/download/{job_id}")
def download_mix(job_id: str):
    job = get_job(job_id)
    if not job or job["status"] != "done":
        return {"error": "Not ready"}
    return FileResponse(job["output"], filename="automix.wav")