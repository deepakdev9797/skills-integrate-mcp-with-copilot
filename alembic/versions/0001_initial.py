"""Initial tables
Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-31 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'activities',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('schedule', sa.String(), nullable=True),
        sa.Column('max_participants', sa.Integer(), nullable=True),
    )
    op.create_table(
        'participants',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'registrations',
        sa.Column('activity_id', sa.Integer(), sa.ForeignKey('activities.id'), primary_key=True),
        sa.Column('participant_id', sa.Integer(), sa.ForeignKey('participants.id'), primary_key=True),
    )


def downgrade():
    op.drop_table('registrations')
    op.drop_table('participants')
    op.drop_table('activities')
