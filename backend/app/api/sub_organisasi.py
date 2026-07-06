from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.i18n import t

from app.schemas.sub_organisasi_schema import (
    SubOrganisasiCreate,
    SubOrganisasiResponse
)

from app.services.sub_organisasi_service import (
    get_sub_by_organisasi,
    create_sub_organisasi,
    update_sub_organisasi,
    delete_sub_organisasi
)

from app.models.sub_organisasi import SubOrganisasi

router = APIRouter(prefix="/sub-organisasi", tags=[t("docs.tags.subOrganization")])


# =========================
# GET (BY ORGANISASI)
# =========================
@router.get("/organisasi/{organisasi_id}", response_model=list[SubOrganisasiResponse])
def get_by_organisasi(organisasi_id: int, db: Session = Depends(get_db)):
    return get_sub_by_organisasi(db, organisasi_id)


# =========================
# GET (BY ID)
# =========================
@router.get("/{id}", response_model=SubOrganisasiResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    sub = db.query(SubOrganisasi).filter(SubOrganisasi.id == id).first()

    if not sub:
        raise HTTPException(status_code=404, detail=t("subOrganization.notFound"))

    return {
        "id": sub.id,
        "organisasi_id": sub.organisasi_id,
        "kod": sub.kod,
        "nama": sub.nama,
        "keterangan": sub.keterangan,
        "pegawai_tadbir": sub.pegawai_tadbir,   # ✅ FIXED
        "jawatan": sub.jawatan,                 # ✅ FIXED
        "aktif": bool(sub.aktif) if sub.aktif is not None else False
    }


# =========================
# CREATE
# =========================
@router.post("/", response_model=SubOrganisasiResponse)
def create(data: SubOrganisasiCreate, db: Session = Depends(get_db)):
    return create_sub_organisasi(db, data.dict())


# =========================
# UPDATE
# =========================
@router.put("/{id}", response_model=SubOrganisasiResponse)
def update(id: int, data: SubOrganisasiCreate, db: Session = Depends(get_db)):
    updated = update_sub_organisasi(db, id, data.dict())

    if not updated:
        raise HTTPException(status_code=404, detail=t("subOrganization.notFound"))

    return updated


# =========================
# DELETE
# =========================
@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_sub_organisasi(db, id)

    if not deleted:
        raise HTTPException(status_code=404, detail=t("subOrganization.notFound"))

    return {"message": t("common.deleted")}
