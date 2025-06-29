"""Initial schema"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=256), nullable=False, unique=True),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="user"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()")),
    )

    op.create_table(
        "transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("from_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("to_user", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(18, 2), nullable=False),
        sa.Column("currency", sa.String(length=8), server_default="USD"),
        sa.Column("status", sa.String(length=16), server_default="PENDING"),
        sa.Column("ts_epoch", sa.DateTime(), server_default=sa.text("now()")),
    )


def downgrade():
    op.drop_table("transactions")
    op.drop_table("users")
