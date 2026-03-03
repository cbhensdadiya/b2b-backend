"""add_category_display_flags

Revision ID: 8fc5ad193230
Revises: 7fc5ad193229
Create Date: 2026-02-25 17:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc5ad193230'
down_revision = '7fc5ad193229'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add show_on_home column to categories table
    op.add_column('categories', sa.Column('show_on_home', sa.Boolean(), nullable=False, server_default='true'))
    
    # Add show_in_menu column to categories table
    op.add_column('categories', sa.Column('show_in_menu', sa.Boolean(), nullable=False, server_default='true'))


def downgrade() -> None:
    # Remove show_in_menu column from categories table
    op.drop_column('categories', 'show_in_menu')
    
    # Remove show_on_home column from categories table
    op.drop_column('categories', 'show_on_home')
