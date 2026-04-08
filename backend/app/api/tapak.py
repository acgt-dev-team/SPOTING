from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base

# ✅ LOAD ALL MODELS ONCE
import app.models

from app.api import tugasan, profil, tapak

app = FastAPI(
    title="SPOTING Backend",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


# ✅ TEMP CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(tugasan.router)
app.include_router(profil.router)
app.include_router(tapak.router)


@app.get("/")
def root():
    return {
        "message": "SPOTING backend running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "ok"}