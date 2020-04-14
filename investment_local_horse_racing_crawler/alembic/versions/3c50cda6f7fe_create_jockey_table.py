"""create jockey table

Revision ID: 3c50cda6f7fe
Revises: c30049fb8722
Create Date: 2020-04-02 04:12:19.241777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c50cda6f7fe'
down_revision = 'c30049fb8722'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "jockey",
        sa.Column("jockey_id", sa.String(255), primary_key=True),
        sa.Column("jockey_name", sa.String(255), nullable=False),
        sa.Column("birthday", sa.DateTime, nullable=False),
        sa.Column("gender", sa.String(255), nullable=False),
        sa.Column("belong_to", sa.String(255), nullable=False),
        sa.Column("first_licensing_year", sa.Integer, nullable=False),
    )


def downgrade():
    pass
