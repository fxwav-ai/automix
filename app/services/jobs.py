import json
import os
import uuid

JOBS_FILE = "/tmp/jobs.json"

def _load_jobs():
    if not os.path.exists(JOBS_FILE):
        return {}
    with open(JOBS_FILE, "r") as f:
        return json.load(f)

def _save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f)

def create_job(track_paths):
    jobs = _load_jobs()
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "tracks": track_paths,
        "output": None
    }

    _save_jobs(jobs)
    return job_id

def update_job(job_id, data):
    jobs = _load_jobs()
    jobs[job_id].update(data)
    _save_jobs(jobs)

def get_job(job_id):
    return _load_jobs().get(job_id)