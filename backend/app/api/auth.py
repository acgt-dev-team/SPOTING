from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth_schema import LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "access_token": "dummy-token",  # 🔥 next phase: JWT
        "role": user.role,
        "pelanggan_id": user.pelanggan_id
    }