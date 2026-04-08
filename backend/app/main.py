from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base

# ✅ SAFE model imports (no aggregation)
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan

# ✅ routers
from app.api import tugasan, profil, tapak

app = FastAPI(
    title="SPOTING Backend",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://seahorse-app-6x2kt.ondigitalocean.app",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ register routers
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

import logging
logging.basicConfig(level=logging.DEBUG)