"""add_image_url_to_categories

Revision ID: 7fc5ad193229
Revises: a69d2d6ed100
Create Date: 2026-02-25 17:03:34.242306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc5ad193229'
down_revision = 'a69d2d6ed100'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add image_url column to categories table
    op.add_column('categories', sa.Column('image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    # Remove image_url column from categories table
    op.drop_column('categories', 'image_url')
