from datetime import datetime, timedelta
import unittest

from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.auth import change_password, login, logout
from app.database.session import Base
from app.dependencies.auth import get_authenticated_user, require_current_user
from app.models.auth_session import AuthSession
from app.models.pelanggan import Pelanggan  # noqa: F401 - registers FK target
from app.models.user import User
from app.schemas.auth_schema import ChangePasswordRequest, LoginRequest
from app.utils.security import is_valid_password, is_valid_user_id, verify_password


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(
            engine,
            tables=[
                Pelanggan.__table__,
                User.__table__,
                AuthSession.__table__,
            ],
        )
        self.db = sessionmaker(bind=engine)()

    def tearDown(self):
        self.db.close()

    def add_user(self, username="valid.user1", **overrides):
        values = {
            "nama": "Test User",
            "username": username,
            "password": "Current1!",
            "role": "user",
            "aktif": True,
            "force_password_change": False,
        }
        values.update(overrides)
        user = User(**values)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def test_user_id_validation(self):
        self.assertTrue(is_valid_user_id("valid.user1"))
        for invalid in (
            "short.id",
            "Valid.user1",
            "valid user1",
            "valid_user1",
            "valid-user1",
        ):
            self.assertFalse(is_valid_user_id(invalid))

    def test_password_validation(self):
        self.assertTrue(is_valid_password("Secure1!"))
        for invalid in (
            "Short1!",
            "lowercase1!",
            "UPPERCASE1!",
            "NoNumber!",
            "NoSpecial1",
        ):
            self.assertFalse(is_valid_password(invalid))

    def test_deleted_account_cannot_log_in(self):
        self.add_user(deleted_at=datetime.utcnow())

        with self.assertRaises(HTTPException) as raised:
            login(LoginRequest(username="valid.user1", password="Current1!"), self.db)

        self.assertEqual(raised.exception.status_code, 404)
        self.assertEqual(raised.exception.detail, "Tiada akaun wujud.")
        self.assertEqual(self.db.query(AuthSession).count(), 0)

    def test_deactivated_account_cannot_log_in(self):
        self.add_user(aktif=False)

        with self.assertRaises(HTTPException) as raised:
            login(LoginRequest(username="valid.user1", password="Current1!"), self.db)

        self.assertEqual(raised.exception.status_code, 403)
        self.assertEqual(
            raised.exception.detail,
            "Akaun telah dinyahaktifkan. Sila hubungi pentadbir sistem untuk bantuan selanjutnya.",
        )
        self.assertEqual(self.db.query(AuthSession).count(), 0)

    def test_logout_revokes_issued_session(self):
        self.add_user()
        result = login(
            LoginRequest(username="valid.user1", password="Current1!"),
            self.db,
        )
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=result["access_token"],
        )

        auth_session = self.db.query(AuthSession).one()
        expected_lifetime = auth_session.expires_at - auth_session.created_at
        self.assertEqual(result["expires_in"], 30 * 60)
        self.assertLessEqual(
            abs(expected_lifetime - timedelta(minutes=30)),
            timedelta(seconds=1),
        )

        logout(credentials, self.db)

        self.db.refresh(auth_session)
        self.assertIsNotNone(auth_session.revoked_at)

        with self.assertRaises(HTTPException) as raised:
            get_authenticated_user(credentials, self.db)
        self.assertEqual(raised.exception.status_code, 401)

    def test_invalid_user_id_is_rejected_by_login(self):
        with self.assertRaises(HTTPException) as raised:
            login(LoginRequest(username="Invalid_ID", password="Current1!"), self.db)

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(self.db.query(AuthSession).count(), 0)

    def test_first_login_is_blocked_until_strong_password_is_set(self):
        user = self.add_user(force_password_change=True)

        with self.assertRaises(HTTPException) as raised:
            require_current_user(user)
        self.assertEqual(raised.exception.status_code, 428)

        with self.assertRaises(HTTPException):
            change_password(ChangePasswordRequest(password="weak"), user, self.db)

        change_password(ChangePasswordRequest(password="NewStrong1!"), user, self.db)
        self.assertFalse(user.force_password_change)
        self.assertTrue(verify_password("NewStrong1!", user.password))

    def test_session_cannot_exceed_thirty_minutes(self):
        self.add_user()
        result = login(
            LoginRequest(username="valid.user1", password="Current1!"),
            self.db,
        )
        auth_session = self.db.query(AuthSession).one()
        auth_session.created_at = datetime.utcnow() - timedelta(minutes=31)
        auth_session.expires_at = datetime.utcnow() + timedelta(hours=7)
        self.db.commit()

        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=result["access_token"],
        )
        with self.assertRaises(HTTPException) as raised:
            get_authenticated_user(credentials, self.db)

        self.assertEqual(raised.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
