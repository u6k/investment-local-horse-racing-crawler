"""init

Revision ID: 7491ceeb5053
Revises: 
Create Date: 2020-10-16 23:46:04.219483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7491ceeb5053'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "calendar_race_url",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("calendar_url", sa.String(255), nullable=False),
        sa.Column("race_url", sa.String(255), nullable=False),
    )


def downgrade():
    pass
