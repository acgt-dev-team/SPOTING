import random
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re

from app.database.session import get_db
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, CreateUserRequest, ProfileUpdateRequest, ProfileResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User account does not exist."
        )

    if not user.aktif:
        raise HTTPException(
            status_code=403,
            detail="Account has been deactivated. Contact the system administrator for further action."
        )

    if user.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

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
    if not re.fullmatch(
        r"[a-z0-9]{12}",
        data.username
    ):
        raise HTTPException(
            status_code=400,
            detail="Username must contain exactly 12 lowercase letters and digits"
        )

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

@router.put("/users/{user_id}/deactivate")
def deactivate_user(
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

    user.aktif = False

    db.commit()

    return {
        "message": "User deactivated"
    }

@router.put("/users/{user_id}/activate")
def activate_user(
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

    user.aktif = True

    db.commit()

    return {
        "message": "User activated"
    }

@router.put("/users/{user_id}/reset-password")
def reset_password(
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

    temp_password = generate_password()

    user.password = temp_password
    user.force_password_change = True

    db.commit()

    return {
        "temporary_password": temp_password
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

@router.get("/profile/{username}")
def get_profile(
    username: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "nama": user.nama,
        "username": user.username,
        "email": user.email,
        "phone": user.phone
    }

@router.put("/profile/{username}")
def update_profile(
    username: str,
    data: ProfileUpdateRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.nama = data.nama
    user.email = data.email
    user.phone = data.phone

    if data.password:
        user.password = data.password

    db.commit()

    return {
        "message": "Profile updated"
    }