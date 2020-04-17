"""create trainer table

Revision ID: a1c68eb6a1f7
Revises: 3c50cda6f7fe
Create Date: 2020-04-02 05:33:53.325151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c68eb6a1f7'
down_revision = '3c50cda6f7fe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "trainer",
        sa.Column("trainer_id", sa.String(255), primary_key=True),
        sa.Column("trainer_name", sa.String(255), nullable=False),
        sa.Column("birthday", sa.DateTime, nullable=False),
        sa.Column("gender", sa.String(255), nullable=False),
        sa.Column("belong_to", sa.String(255), nullable=False),
    )


def downgrade():
    pass
