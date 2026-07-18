import base64
import hashlib
import hmac
import os
import re
import secrets


PASSWORD_HASH_PREFIX = "pbkdf2_sha256"
PASSWORD_HASH_ITERATIONS = 600_000
SALT_BYTES = 16
USER_ID_PATTERN = re.compile(r"^[a-z0-9.]{10,24}$")

try:
    SESSION_LIFETIME_MINUTES = max(
        1,
        int(os.getenv("SESSION_LIFETIME_MINUTES", "30")),
    )
except ValueError:
    SESSION_LIFETIME_MINUTES = 30


def is_valid_user_id(user_id: str) -> bool:
    return bool(USER_ID_PATTERN.fullmatch(user_id))


def is_valid_password(password: str) -> bool:
    return (
        len(password) >= 8
        and bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[a-z]", password))
        and bool(re.search(r"[0-9]", password))
        and bool(re.search(r"[^A-Za-z0-9]", password))
    )


def generate_session_token() -> str:
    return secrets.token_urlsafe(48)


def hash_session_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_HASH_ITERATIONS,
    )

    salt_b64 = base64.b64encode(salt).decode("ascii")
    digest_b64 = base64.b64encode(digest).decode("ascii")

    return (
        f"{PASSWORD_HASH_PREFIX}"
        f"${PASSWORD_HASH_ITERATIONS}"
        f"${salt_b64}"
        f"${digest_b64}"
    )


def is_password_hashed(password: str) -> bool:
    return password.startswith(f"{PASSWORD_HASH_PREFIX}$")


def verify_password(plain_password: str, stored_password: str) -> bool:
    if not is_password_hashed(stored_password):
        return hmac.compare_digest(stored_password, plain_password)

    try:
        _, iterations, salt_b64, digest_b64 = stored_password.split("$", 3)
        iterations = int(iterations)
        salt = base64.b64decode(salt_b64)
        stored_digest = base64.b64decode(digest_b64)
    except (ValueError, TypeError):
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt,
        iterations,
    )

    return hmac.compare_digest(stored_digest, digest)
