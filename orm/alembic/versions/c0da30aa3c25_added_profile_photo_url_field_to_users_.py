"""added profile photo url field to users db

Revision ID: c0da30aa3c25
Revises: e26ed6f0ffcb
Create Date: 2026-04-18 13:43:24.936622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c0da30aa3c25'
down_revision: Union[str, Sequence[str], None] = 'e26ed6f0ffcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('profile_picture_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'profile_picture_url')
