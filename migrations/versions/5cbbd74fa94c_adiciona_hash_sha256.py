"""adiciona hash_sha256

Revision ID: 5cbbd74fa94c
Revises: 0001
Create Date: 2026-10-13 15:59:01.022547
"""
from alembic import op
import sqlalchemy as sa


revision = '5cbbd74fa94c'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("arquivos", sa.Column("hash_sha256", sa.String(64)))
    op.create_index("ix_arquivos_hash_sha256", "arquivos", ["hash_sha256"])


def downgrade():
    op.drop_index("ix_arquivos_hash_sha256", table_name="arquivos")
    op.drop_column("arquivos", "hash_sha256")
