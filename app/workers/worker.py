import time
import os
from app.services.jobs import get_job, update_job
from app.services.render_mix import mix_tracks

OUTPUT_DIR = "/tmp/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("🎧 AutoMix worker running")

    while True:
        jobs = get_all_jobs()
        for job_id, job in jobs.items():
            if job["status"] == "queued":
                try:
                    update_job(job_id, {"status": "processing"})
                    output_path = f"{OUTPUT_DIR}/{job_id}.wav"

                    mix_tracks(job["tracks"], output_path)

                    update_job(job_id, {
                        "status": "done",
                        "output": output_path
                    })
                except Exception as e:
                    update_job(job_id, {
                        "status": "error",
                        "error": str(e)
                    })

        time.sleep(3)

def get_all_jobs():
    import json
    if not os.path.exists("/tmp/jobs.json"):
        return {}
    with open("/tmp/jobs.json") as f:
        return json.load(f)

if __name__ == "__main__":
    main()