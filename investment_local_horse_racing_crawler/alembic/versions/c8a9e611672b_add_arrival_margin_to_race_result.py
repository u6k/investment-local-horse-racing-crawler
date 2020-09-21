"""add arrival_margin to race_result

Revision ID: c8a9e611672b
Revises: 1d288fd81741
Create Date: 2020-09-20 05:37:27.655144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c8a9e611672b'
down_revision = '1d288fd81741'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("race_result", sa.Column("arrival_margin", sa.String(255), nullable=True))
    op.add_column("race_result", sa.Column("corner_passing_order", sa.String(255), nullable=True))


def downgrade():
    pass
