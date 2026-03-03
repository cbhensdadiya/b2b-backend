"""add firebase_uid to users

Revision ID: 20260303_firebase_uid
Revises: a9bde1ae2c6e
Create Date: 2026-03-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260303_firebase_uid'
down_revision = 'a9bde1ae2c6e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add firebase_uid column to users table
    op.add_column('users', sa.Column('firebase_uid', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_firebase_uid'), 'users', ['firebase_uid'], unique=True)


def downgrade() -> None:
    # Remove firebase_uid column from users table
    op.drop_index(op.f('ix_users_firebase_uid'), table_name='users')
    op.drop_column('users', 'firebase_uid')
