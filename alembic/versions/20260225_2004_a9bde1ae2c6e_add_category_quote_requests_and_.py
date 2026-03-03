"""add_category_quote_requests_and_followups

Revision ID: a9bde1ae2c6e
Revises: 8fc5ad193230
Create Date: 2026-02-25 20:04:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a9bde1ae2c6e'
down_revision: Union[str, None] = '8fc5ad193230'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create category_quote_requests table
    op.create_table(
        'category_quote_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('categories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('subcategory_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('buyer_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create indexes
    op.create_index('idx_quote_requests_category', 'category_quote_requests', ['category_id'])
    op.create_index('idx_quote_requests_buyer', 'category_quote_requests', ['buyer_id'])
    op.create_index('idx_quote_requests_status', 'category_quote_requests', ['status'])
    op.create_index('idx_quote_requests_created', 'category_quote_requests', ['created_at'])

    # Create quote_request_followups table
    op.create_table(
        'quote_request_followups',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('quote_request_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('category_quote_requests.id', ondelete='CASCADE'), nullable=False),
        sa.Column('admin_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('followup_text', sa.Text, nullable=False),
        sa.Column('status', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
    )

    # Create indexes
    op.create_index('idx_followups_quote_request', 'quote_request_followups', ['quote_request_id'])
    op.create_index('idx_followups_admin', 'quote_request_followups', ['admin_id'])
    op.create_index('idx_followups_created', 'quote_request_followups', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_followups_created', table_name='quote_request_followups')
    op.drop_index('idx_followups_admin', table_name='quote_request_followups')
    op.drop_index('idx_followups_quote_request', table_name='quote_request_followups')
    op.drop_table('quote_request_followups')
    
    op.drop_index('idx_quote_requests_created', table_name='category_quote_requests')
    op.drop_index('idx_quote_requests_status', table_name='category_quote_requests')
    op.drop_index('idx_quote_requests_buyer', table_name='category_quote_requests')
    op.drop_index('idx_quote_requests_category', table_name='category_quote_requests')
    op.drop_table('category_quote_requests')
