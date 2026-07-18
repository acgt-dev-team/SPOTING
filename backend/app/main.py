from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.session import engine, Base
from app.i18n import t

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
from app.models.ejen import Ejen
from app.models.hasil_imbasan import HasilImbasan
from app.models.auth_session import AuthSession
from app.dependencies.auth import require_current_user

from app.scheduler.profile_scheduler import scheduler, load_profile_jobs
from app.api import report
from app.api import dashboard

# ✅ Routers ONLY from API
from app.api import (
    tugasan,
    profil,
    tapak,
    sub_organisasi,
    organisasi,
    jenis_tugasan,
    auth,
    ejen,
    hasil_imbasan,
)

app = FastAPI(
    title=t("app.title"),
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ONLY API routers
protected_dependencies = [Depends(require_current_user)]

app.include_router(tugasan.router, dependencies=protected_dependencies)
app.include_router(profil.router, dependencies=protected_dependencies)
app.include_router(tapak.router, dependencies=protected_dependencies)
app.include_router(sub_organisasi.router, dependencies=protected_dependencies)
app.include_router(organisasi.router, dependencies=protected_dependencies)
app.include_router(jenis_tugasan.router, dependencies=protected_dependencies)
app.include_router(auth.router)
# Agent endpoints remain independent because installed scanning agents do not
# participate in browser user sessions.
app.include_router(ejen.router)
app.include_router(hasil_imbasan.router)
app.include_router(report.router, dependencies=protected_dependencies)
app.include_router(dashboard.router, dependencies=protected_dependencies)



@app.get("/")
def root():
    return {
        "message": t("app.running"),
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
