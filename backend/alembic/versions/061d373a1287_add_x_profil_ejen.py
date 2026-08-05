"""add x_profil_ejen

Revision ID: 061d373a1287
Revises: 60cdff2fd733
Create Date: 2026-08-05 13:12:47.084569

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

"""add x_profil_ejen

Revision ID: 061d373a1287
Revises: 60cdff2fd733
Create Date: 2026-08-05 13:12:47.084569
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "061d373a1287"
down_revision: Union[str, Sequence[str], None] = "60cdff2fd733"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "x_profil_ejen",

        sa.Column(
            "id",
            sa.BigInteger(),
            primary_key=True
        ),

        sa.Column(
            "profil_id",
            sa.BigInteger(),
            nullable=False
        ),

        sa.Column(
            "ejen_id",
            sa.BigInteger(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(20),
            nullable=False,
            server_default="Pending"
        ),

        sa.Column(
            "started_at",
            sa.TIMESTAMP(),
            nullable=True
        ),

        sa.Column(
            "completed_at",
            sa.TIMESTAMP(),
            nullable=True
        ),

        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("now()")
        ),

        sa.ForeignKeyConstraint(
            ["profil_id"],
            ["profil.id"],
            ondelete="CASCADE"
        ),

        sa.ForeignKeyConstraint(
            ["ejen_id"],
            ["ejen.id"],
            ondelete="CASCADE"
        ),

        sa.UniqueConstraint(
            "profil_id",
            "ejen_id",
            name="uq_x_profil_ejen"
        ),
    )


def downgrade() -> None:

    op.drop_table("x_profil_ejen")
