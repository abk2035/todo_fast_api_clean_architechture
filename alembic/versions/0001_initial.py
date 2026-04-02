"""Initial models

Revision ID: 0001
Revises: 
Create Date: 2026-03-29 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# identifiants de révision, utilisés par Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=180), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
    )
    op.create_table(
        'todo',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=True, server_default=sa.text('false')),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('user.id'), nullable=False),
    )


def downgrade():
    op.drop_table('todo')
    op.drop_table('user')
