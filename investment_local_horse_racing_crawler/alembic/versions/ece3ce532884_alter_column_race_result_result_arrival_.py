"""alter column race_result result/arrival_time

Revision ID: ece3ce532884
Revises: db6db4289e1b
Create Date: 2020-04-02 16:59:48.281753

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'ece3ce532884'
down_revision = 'db6db4289e1b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_result", "result", nullable=True)
    op.alter_column("race_result", "arrival_time", nullable=True)


def downgrade():
    pass
