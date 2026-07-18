from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.i18n import t
from app.models.auth_session import AuthSession
from app.models.user import User
from app.utils.security import SESSION_LIFETIME_MINUTES, hash_session_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_authenticated_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise _unauthorized(t("auth.authenticationRequired"))

    session = (
        db.query(AuthSession)
        .filter(
            AuthSession.token_hash == hash_session_token(credentials.credentials),
            AuthSession.revoked_at.is_(None),
            AuthSession.expires_at > datetime.utcnow(),
            AuthSession.created_at
            > datetime.utcnow() - timedelta(minutes=SESSION_LIFETIME_MINUTES),
        )
        .first()
    )

    if session is None:
        raise _unauthorized(t("auth.sessionInvalid"))

    user = db.query(User).filter(User.id == session.user_id).first()

    if user is None or user.deleted_at is not None:
        raise _unauthorized(t("auth.accountNotFound"))

    if not user.aktif:
        raise _unauthorized(t("auth.accountDeactivated"))

    return user


def require_current_user(
    user: User = Depends(get_authenticated_user),
) -> User:
    if user.force_password_change:
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail=t("auth.passwordChangeRequired"),
        )

    return user


def require_admin_user(
    user: User = Depends(require_current_user),
) -> User:
    if user.role not in {"admin", "super admin"}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=t("auth.forbidden"),
        )

    return user


def revoke_user_sessions(db: Session, user_id: int) -> None:
    db.query(AuthSession).filter(
        AuthSession.user_id == user_id,
        AuthSession.revoked_at.is_(None),
    ).update(
        {AuthSession.revoked_at: datetime.utcnow()},
        synchronize_session=False,
    )


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
