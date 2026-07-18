"""add secure auth sessions and soft-deleted users

Revision ID: d7f6b2c9a104
Revises: a961b45f67b5
Create Date: 2026-07-18 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d7f6b2c9a104"
down_revision: Union[str, Sequence[str], None] = "a961b45f67b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    inspector = sa.inspect(op.get_bind())
    table_names = set(inspector.get_table_names())

    # The historical SQL dump contained users before Alembic began managing
    # that table. Creating it conditionally keeps both existing and fresh
    # installations upgradeable.
    if "users" not in table_names:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("nama", sa.String(), nullable=False),
            sa.Column("username", sa.String(length=24), nullable=False),
            sa.Column("password", sa.String(), nullable=False),
            sa.Column("role", sa.String(), nullable=True),
            sa.Column("aktif", sa.Boolean(), nullable=True),
            sa.Column("force_password_change", sa.Boolean(), nullable=True),
            sa.Column("deleted_at", sa.DateTime(), nullable=True),
            sa.Column("email", sa.String(), nullable=True),
            sa.Column("phone", sa.String(), nullable=True),
            sa.Column("pelanggan_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(["pelanggan_id"], ["pelanggan.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("username"),
        )
        op.create_index("ix_users_id", "users", ["id"], unique=False)
    else:
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "deleted_at" not in user_columns:
            op.add_column(
                "users", sa.Column("deleted_at", sa.DateTime(), nullable=True)
            )

    op.create_table(
        "auth_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_auth_sessions_id", "auth_sessions", ["id"], unique=False)
    op.create_index(
        "ix_auth_sessions_token_hash",
        "auth_sessions",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        "ix_auth_sessions_user_id", "auth_sessions", ["user_id"], unique=False
    )
    op.create_index(
        "ix_auth_sessions_expires_at",
        "auth_sessions",
        ["expires_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_auth_sessions_expires_at", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_user_id", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_token_hash", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_id", table_name="auth_sessions")
    op.drop_table("auth_sessions")
    inspector = sa.inspect(op.get_bind())
    if "users" in inspector.get_table_names():
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "deleted_at" in user_columns:
            op.drop_column("users", "deleted_at")
