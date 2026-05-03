from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, CreateUserRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "access_token": "dummy-token",  # next phase: JWT
        "role": user.role,
        "pelanggan_id": user.pelanggan_id
    }

@router.post("/users")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        nama=data.nama,
        username=data.username,
        password=data.password,
        role=data.role,
        aktif=data.aktif,
        pelanggan_id=data.pelanggan_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }

@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = (
        db.query(User)
        .filter(User.role != "super admin")
        .all()
    )

    return users

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.nama = data.nama
    user.username = data.username
    user.password = data.password
    user.role = data.role
    user.aktif = data.aktif

    db.commit()

    return {
        "message": "User updated"
    }

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted"
    }