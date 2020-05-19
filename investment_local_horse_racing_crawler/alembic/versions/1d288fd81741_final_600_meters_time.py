"""final 600 meters time

Revision ID: 1d288fd81741
Revises: 48692020e3af
Create Date: 2020-05-20 01:12:00.559250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d288fd81741'
down_revision = '48692020e3af'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("race_result", sa.Column("final_600_meters_time", sa.Float, nullable=True))


def downgrade():
    pass
