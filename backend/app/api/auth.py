from datetime import datetime, timedelta
import secrets
import string

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import (
    bearer_scheme,
    get_authenticated_user,
    require_admin_user,
    require_current_user,
    revoke_user_sessions,
)
from app.i18n import t
from app.models.auth_session import AuthSession
from app.models.user import User
from app.schemas.auth_schema import (
    ChangePasswordRequest,
    CreateUserRequest,
    LoginRequest,
    ProfileResponse,
    ProfileUpdateRequest,
    UserResponse,
)
from app.utils.security import (
    generate_session_token,
    hash_password,
    hash_session_token,
    is_password_hashed,
    is_valid_password,
    is_valid_user_id,
    SESSION_LIFETIME_MINUTES,
    verify_password,
)


router = APIRouter(prefix="/auth", tags=[t("docs.tags.auth")])

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    _validate_user_id(data.username)

    user = db.query(User).filter(User.username == data.username).first()

    # Account state is deliberately checked before the password so deleted and
    # deactivated accounts can never receive a session.
    if user is None or user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=t("auth.accountNotFound"),
        )

    if not user.aktif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=t("auth.accountDeactivated"),
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=t("auth.invalidPassword"),
        )

    if not is_password_hashed(user.password):
        user.password = hash_password(data.password)

    access_token = generate_session_token()
    expires_at = datetime.utcnow() + timedelta(minutes=SESSION_LIFETIME_MINUTES)
    db.add(
        AuthSession(
            token_hash=hash_session_token(access_token),
            user_id=user.id,
            created_at=datetime.utcnow(),
            expires_at=expires_at,
        )
    )
    db.commit()

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": SESSION_LIFETIME_MINUTES * 60,
        "role": user.role,
        "pelanggan_id": user.pelanggan_id,
        "force_password_change": user.force_password_change,
    }


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is not None and credentials.scheme.lower() == "bearer":
        session = (
            db.query(AuthSession)
            .filter(
                AuthSession.token_hash
                == hash_session_token(credentials.credentials),
                AuthSession.revoked_at.is_(None),
            )
            .first()
        )

        if session is not None:
            session.revoked_at = datetime.utcnow()
            db.commit()

    # Idempotent logout lets the frontend safely clear local state even when a
    # session has already expired or been revoked elsewhere.
    return {"message": t("auth.loggedOut")}


@router.get("/session")
def get_session(user: User = Depends(get_authenticated_user)):
    return {
        "username": user.username,
        "role": user.role,
        "pelanggan_id": user.pelanggan_id,
        "force_password_change": user.force_password_change,
    }


@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    user: User = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    _validate_password(data.password)

    user.password = hash_password(data.password)
    user.force_password_change = False
    db.commit()

    return {"message": t("auth.passwordUpdated")}


@router.post("/users")
def create_user(
    data: CreateUserRequest,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    _validate_user_id(data.username)

    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=t("auth.usernameExists"),
        )

    generated_password = generate_password()
    new_user = User(
        nama=data.nama,
        username=data.username,
        password=hash_password(generated_password),
        role=data.role,
        aktif=data.aktif,
        pelanggan_id=data.pelanggan_id,
        force_password_change=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": t("auth.userCreated"),
        "generated_password": generated_password,
    }


@router.get("/users", response_model=list[UserResponse])
def get_users(
    role: str,
    current_user: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.deleted_at.is_(None))

    if current_user.role == "super admin":
        return query.filter(User.role != "super admin").all()

    return query.filter(User.role == "user").all()


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: CreateUserRequest,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    user = _get_available_user(db, user_id)
    _validate_user_id(data.username)

    existing = (
        db.query(User)
        .filter(User.username == data.username, User.id != user_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=t("auth.usernameExists"),
        )

    user.nama = data.nama
    user.username = data.username
    user.role = data.role
    user.aktif = data.aktif
    db.commit()

    return {"message": t("auth.userUpdated")}


@router.put("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    user = _get_available_user(db, user_id)
    user.aktif = False
    revoke_user_sessions(db, user.id)
    db.commit()

    return {"message": t("auth.userDeactivated")}


@router.put("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    user = _get_available_user(db, user_id)
    temporary_password = generate_password()
    user.aktif = True
    user.password = hash_password(temporary_password)
    user.force_password_change = True
    revoke_user_sessions(db, user.id)
    db.commit()

    return {
        "message": t("auth.userActivated"),
        "temporary_password": temporary_password,
        "force_password_change": True,
    }


@router.put("/users/{user_id}/reset-password")
def reset_password(
    user_id: int,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    user = _get_available_user(db, user_id)
    temporary_password = generate_password()
    user.password = hash_password(temporary_password)
    user.force_password_change = True
    revoke_user_sessions(db, user.id)
    db.commit()

    return {"temporary_password": temporary_password}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    _: User = Depends(require_admin_user),
    db: Session = Depends(get_db),
):
    user = _get_available_user(db, user_id)
    user.deleted_at = datetime.utcnow()
    user.aktif = False
    revoke_user_sessions(db, user.id)
    db.commit()

    return {"message": t("auth.userDeleted")}


@router.get("/profile/{username}", response_model=ProfileResponse)
def get_profile(
    username: str,
    current_user: User = Depends(require_current_user),
):
    _ensure_own_profile(username, current_user)
    return current_user


@router.put("/profile/{username}")
def update_profile(
    username: str,
    data: ProfileUpdateRequest,
    current_user: User = Depends(require_current_user),
    db: Session = Depends(get_db),
):
    _ensure_own_profile(username, current_user)

    current_user.nama = data.nama
    current_user.email = data.email
    current_user.phone = data.phone

    if data.password:
        _validate_password(data.password)
        current_user.password = hash_password(data.password)

    db.commit()
    return {"message": t("auth.profileUpdated")}


def generate_password(length: int = 12) -> str:
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    symbols = "!@#$%^&*"
    all_chars = lowercase + uppercase + numbers + symbols

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(numbers),
        secrets.choice(symbols),
    ]
    password += [secrets.choice(all_chars) for _ in range(length - 4)]
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


def _get_available_user(db: Session, user_id: int) -> User:
    user = (
        db.query(User)
        .filter(User.id == user_id, User.deleted_at.is_(None))
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=t("auth.userNotFound"),
        )
    return user


def _validate_user_id(user_id: str) -> None:
    if not is_valid_user_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=t("auth.usernameInvalid"),
        )


def _validate_password(password: str) -> None:
    if not is_valid_password(password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=t("auth.passwordInvalid"),
        )


def _ensure_own_profile(username: str, current_user: User) -> None:
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=t("auth.forbidden"),
        )
