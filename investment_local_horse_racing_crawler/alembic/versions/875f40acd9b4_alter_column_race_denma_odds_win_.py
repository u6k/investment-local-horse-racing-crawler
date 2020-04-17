"""alter column race_denma odds_win/favorite nullable

Revision ID: 875f40acd9b4
Revises: 7434e3253fe7
Create Date: 2020-04-02 12:56:36.525352

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '875f40acd9b4'
down_revision = '7434e3253fe7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("race_denma", "odds_win", nullable=True)
    op.alter_column("race_denma", "favorite", nullable=True)


def downgrade():
    pass
