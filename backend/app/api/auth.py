import secrets
import string
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import re

from app.database.session import get_db
from app.i18n import t
from app.models.user import User
from app.schemas.auth_schema import LoginRequest, CreateUserRequest, ProfileUpdateRequest, ProfileResponse
from app.utils.security import hash_password, is_password_hashed, verify_password

router = APIRouter(prefix="/auth", tags=[t("docs.tags.auth")])


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
            detail=t("auth.accountNotFound")
        )

    if not user.aktif:
        raise HTTPException(
            status_code=403,
            detail=t("auth.accountDeactivated")
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail=t("auth.invalidPassword")
        )

    if not is_password_hashed(user.password):
        user.password = hash_password(data.password)
        db.commit()

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
            detail=t("auth.userNotFound")
        )

    user.password = hash_password(data.password)
    user.force_password_change = False

    db.commit()

    return {
        "message": t("auth.passwordUpdated")
    }

@router.post("/users")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db)
):
    if not re.fullmatch(
        r"[a-z0-9.]{12,24}",
        data.username
    ):
        raise HTTPException(
            status_code=400,
            detail=t("auth.usernameInvalid")
        )

    existing = db.query(User).filter(
        User.username == data.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=t("auth.usernameExists")
        )
    generated_password = generate_password()

    new_user = User(
        nama=data.nama,
        username=data.username,
        password=hash_password(generated_password),
        role=data.role,
        aktif=data.aktif,
        pelanggan_id=data.pelanggan_id,
        force_password_change=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
    "message": t("auth.userCreated"),
    "generated_password": generated_password
}

@router.get("/users")
def get_users(
    role: str,
    db: Session = Depends(get_db)
):

    if role == "super admin":

        users = (
            db.query(User)
            .filter(User.role != "super admin")
            .all()
        )

    else:

        users = (
            db.query(User)
            .filter(User.role == "user")
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
            detail=t("auth.userNotFound")
        )
    
    if not re.fullmatch(
        r"[a-z0-9.]{12,24}",
        data.username
    ):
        raise HTTPException(
            status_code=400,
            detail="Username mesti mengandungi 12 hingga 24 aksara dan hanya huruf kecil, nombor atau tanda titik (.)"
        )

    user.nama = data.nama
    user.username = data.username
    user.role = data.role
    user.aktif = data.aktif

    db.commit()

    return {
        "message": t("auth.userUpdated")
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
            detail=t("auth.userNotFound")
        )

    user.aktif = False

    db.commit()

    return {
        "message": t("auth.userDeactivated")
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
            detail=t("auth.userNotFound")
        )

    user.aktif = True

    db.commit()

    return {
        "message": t("auth.userActivated")
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
            detail=t("auth.userNotFound")
        )

    temp_password = generate_password()

    user.password = hash_password(temp_password)
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
            detail=t("auth.userNotFound")
        )

    db.delete(user)
    db.commit()

    return {
        "message": t("auth.userDeleted")
    }


def generate_password(length=12):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = "!@#$%^&*"

    all_chars = lowercase + uppercase + numbers + symbols

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(numbers),
        secrets.choice(symbols)
    ]

    password += [
        secrets.choice(all_chars)
        for _ in range(length - 4)
    ]

    secrets.SystemRandom().shuffle(password)

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
            detail=t("auth.userNotFound")
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
            detail=t("auth.userNotFound")
        )

    user.nama = data.nama
    user.email = data.email
    user.phone = data.phone

    if data.password:
        user.password = hash_password(data.password)

    db.commit()

    return {
        "message": t("auth.profileUpdated")
    }
