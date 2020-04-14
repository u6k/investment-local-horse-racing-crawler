"""alter column weather nullable

Revision ID: 4ab9c2463441
Revises: e40fe886d29e
Create Date: 2020-04-08 15:43:13.181898

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '4ab9c2463441'
down_revision = 'e40fe886d29e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_info", "weather", nullable=True)


def downgrade():
    pass
