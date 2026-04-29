from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base

# ✅ Load models (for ORM registration)
from app.models.tapak import Tapak
from app.models.profil import Profil
from app.models.tugasan import Tugasan
from app.models.x_profil_tugasan import XProfilTugasan
from app.models.organisasi import Organisasi
from app.models.sub_organisasi import SubOrganisasi
from app.models.pelanggan import Pelanggan
from app.models.user import User
from app.models.status import Status
from app.api import hasil_imbasan
from app.scheduler.profile_scheduler import scheduler, load_profile_jobs
from app.api import report

# ✅ Routers ONLY from API
from app.api import tugasan, profil, tapak, sub_organisasi, organisasi, jenis_tugasan
from app.api import auth

app = FastAPI(
    title="SPOTING Backend",
    version="1.0.0"
)

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

# ✅ ONLY API routers
app.include_router(tugasan.router)
app.include_router(profil.router)
app.include_router(tapak.router)
app.include_router(sub_organisasi.router)
app.include_router(organisasi.router)
app.include_router(jenis_tugasan.router)
app.include_router(auth.router)
app.include_router(hasil_imbasan.router)
app.include_router(report.router)

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


@app.on_event("startup")
def start_scheduler():
    load_profile_jobs()

    if not scheduler.running:
        scheduler.start()

    print("Scheduler started successfully")