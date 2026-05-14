import random
import string
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
    "access_token": "dummy-token",
    "role": user.role,
    "pelanggan_id": user.pelanggan_id,
    "force_password_change": user.force_password_change
}

@router.post("/change-password")
def change_password(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = data.password
    user.force_password_change = False

    db.commit()

    return {
        "message": "Password updated successfully"
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
    generated_password = generate_password()

    new_user = User(
        nama=data.nama,
        username=data.username,
        password=generated_password,
        role=data.role,
        aktif=data.aktif,
        pelanggan_id=data.pelanggan_id,
        force_password_change=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "message": "User created successfully",
    "generated_password": generated_password
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


def generate_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = "!@#$%^&*"

    all_chars = lowercase + uppercase + numbers + symbols

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(numbers),
        random.choice(symbols)
    ]

    password += random.choices(all_chars, k=length - 4)

    random.shuffle(password)

    return ''.join(password)