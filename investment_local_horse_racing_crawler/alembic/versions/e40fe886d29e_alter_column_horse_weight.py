"""alter column horse_weight

Revision ID: e40fe886d29e
Revises: ece3ce532884
Create Date: 2020-04-08 14:50:38.580894

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'e40fe886d29e'
down_revision = 'ece3ce532884'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_denma", "horse_weight", nullable=True)
    op.alter_column("race_denma", "horse_weight_diff", nullable=True)


def downgrade():
    pass
