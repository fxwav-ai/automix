from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to Lovable domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="AutoMix API", version="1.0")

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}