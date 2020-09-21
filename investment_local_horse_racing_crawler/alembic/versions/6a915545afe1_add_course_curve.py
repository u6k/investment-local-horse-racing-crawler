"""add course curve

Revision ID: 6a915545afe1
Revises: c8a9e611672b
Create Date: 2020-09-21 06:45:42.134597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a915545afe1'
down_revision = 'c8a9e611672b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("race_info", sa.Column("course_curve", sa.String(255), nullable=True))


def downgrade():
    pass
