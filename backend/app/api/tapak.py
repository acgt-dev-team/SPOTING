from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.i18n import t

from app.schemas.tapak_schema import TapakCreate, TapakResponse

from app.services.tapak_service import (
    get_tapak_by_sub,
    create_tapak,
    update_tapak,
    delete_tapak
)

router = APIRouter(prefix="/tapak", tags=[t("docs.tags.site")])


# =========================
# GET
# =========================
@router.get("/sub/{sub_id}", response_model=list[TapakResponse])
def get_by_sub(sub_id: int, db: Session = Depends(get_db)):
    return get_tapak_by_sub(db, sub_id)


# =========================
# CREATE
# =========================
@router.post("/", response_model=TapakResponse)
def create(data: TapakCreate, db: Session = Depends(get_db)):
    return create_tapak(db, data.dict())


# =========================
# UPDATE
# =========================
@router.put("/{id}", response_model=TapakResponse)
def update(id: int, data: TapakCreate, db: Session = Depends(get_db)):
    updated = update_tapak(db, id, data.dict())

    if not updated:
        raise HTTPException(status_code=404, detail=t("site.notFound"))

    return updated


# =========================
# DELETE
# =========================
@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    deleted = delete_tapak(db, id)

    if not deleted:
        raise HTTPException(status_code=404, detail=t("site.notFound"))

    return {"message": t("common.deleted")}

@router.get("/{id}")
def get_one(id: int, db: Session = Depends(get_db)):
    from app.models.tapak import Tapak

    tapak = db.query(Tapak).filter(Tapak.id == id).first()

    if not tapak:
        return {"message": t("common.notFound")}

    return {
    "id": tapak.id,
    "sub_organisasi_id": tapak.sub_organisasi_id,
    "kod": tapak.kod,
    "nama": tapak.nama,
    "keterangan": tapak.keterangan,
    "pegawai_tadbir": tapak.pegawai_tadbir,
    "jawatan": tapak.jawatan,
    "aktif": bool(tapak.aktif) if tapak.aktif is not None else False
}
