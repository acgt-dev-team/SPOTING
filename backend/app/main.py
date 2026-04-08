from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base
from app.api import tugasan, profil, tapak
from app.models import Tapak, Profil, Tugasan, XProfilTugasan

app = FastAPI(
title="SPOTING Backend",
version="1.0.0"
)

# ✅ Create tables on startup (temporary for dev)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# ✅ CORS (allow frontend)

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

# ✅ Register routers

app.include_router(tugasan.router)
app.include_router(profil.router)
app.include_router(tapak.router)

# ✅ Root endpoint

@app.get("/")
def root():
    return {
        "message": "SPOTING backend running",
        "version": "1.0.0"
    }

# ✅ Health check (important for DigitalOcean)

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

import logging

logging.basicConfig(level=logging.DEBUG)