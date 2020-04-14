"""alter column moisture nullable

Revision ID: 7434e3253fe7
Revises: a1c68eb6a1f7
Create Date: 2020-04-02 11:48:12.145179

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '7434e3253fe7'
down_revision = 'a1c68eb6a1f7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_info", "moisture", nullable=True)


def downgrade():
    pass
