"""
Revision ID: 546a776504ea
Revises: 707822367856
Create Date: 2025-09-10 13:06:12.694697

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "546a776504ea"
down_revision = "707822367856"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop old column
    op.drop_column("document_chunks", "embedding")

    # Add new column with 768 dimensions
    op.execute("ALTER TABLE document_chunks ADD COLUMN embedding vector(768)")


def downgrade() -> None:
    # Revert back to 3072 if needed
    op.drop_column("document_chunks", "embedding")
    op.execute("ALTER TABLE document_chunks ADD COLUMN embedding vector(3072)")
