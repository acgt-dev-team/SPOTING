from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.wizard_schema import WizardSetup
from app.services.wizard_service import create_wizard_setup

# Spaces upload
from app.utils.spaces import upload_text_file

router = APIRouter(
    prefix="/wizard",
    tags=["Wizard"]
)


# -----------------------------
# Wizard Setup (MAIN API)
# -----------------------------
@router.post("/setup")
def wizard_setup(
    data: WizardSetup,
    db: Session = Depends(get_db)
):
    """
    Create full wizard hierarchy:
    Pelanggan → Organisasi → SubOrganisasi → Tapak → Profil → Tugasan
    """

    result = create_wizard_setup(db, data)

    return result


# -----------------------------
# LIST ENDPOINTS (FOR DEMO)
# -----------------------------
@router.get("/pelanggan")
def list_pelanggan(db: Session = Depends(get_db)):
    from app.models.pelanggan import Pelanggan
    return db.query(Pelanggan).all()


@router.get("/organisasi/{pelanggan_id}")
def list_organisasi(pelanggan_id: int, db: Session = Depends(get_db)):
    from app.models.organisasi import Organisasi
    return db.query(Organisasi).filter(
        Organisasi.pelanggan_id == pelanggan_id
    ).all()


@router.get("/sub-organisasi/{organisasi_id}")
def list_sub_organisasi(organisasi_id: int, db: Session = Depends(get_db)):
    from app.models.sub_organisasi import SubOrganisasi
    return db.query(SubOrganisasi).filter(
        SubOrganisasi.organisasi_id == organisasi_id
    ).all()


@router.get("/tapak/{sub_id}")
def list_tapak(sub_id: int, db: Session = Depends(get_db)):
    from app.models.tapak import Tapak
    return db.query(Tapak).filter(
        Tapak.sub_organisasi_id == sub_id
    ).all()


@router.get("/profil/{tapak_id}")
def list_profil(tapak_id: int, db: Session = Depends(get_db)):
    from app.models.profil import Profil
    return db.query(Profil).filter(
        Profil.tapak_id == tapak_id
    ).all()


# -----------------------------
# TEST SPACES UPLOAD (IMPORTANT)
# -----------------------------
@router.get("/test-upload")
def test_upload():
    """
    Test upload to DigitalOcean Spaces
    """

    file_url = upload_text_file(
        filename="test.txt",
        content="Hello from SPOTING backend 🚀"
    )

    return {
        "message": "Upload successful",
        "file_url": file_url
    }