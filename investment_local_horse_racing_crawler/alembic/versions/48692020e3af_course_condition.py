"""course_condition

Revision ID: 48692020e3af
Revises: d93402dd9094
Create Date: 2020-05-20 00:05:13.160242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48692020e3af'
down_revision = 'd93402dd9094'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("race_info", sa.Column("course_condition", sa.String(255), nullable=True))


def downgrade():
    pass
