"""alter table race_payoff favorite

Revision ID: d93402dd9094
Revises: 4ab9c2463441
Create Date: 2020-04-17 18:58:13.419878

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd93402dd9094'
down_revision = '4ab9c2463441'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_payoff", "favorite", nullable=True)


def downgrade():
    pass
