"""create odds_win_place table

Revision ID: 27099e810beb
Revises: 55046d809d90
Create Date: 2020-03-30 15:19:25.078784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27099e810beb'
down_revision = '55046d809d90'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "odds_win",
        sa.Column("odds_win_id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=False),
        sa.Column("horse_number", sa.Integer, nullable=False),
        sa.Column("horse_id", sa.String(255), nullable=False),
        sa.Column("odds_win", sa.Float, nullable=False),
    )

    op.create_table(
        "odds_place",
        sa.Column("odds_place_id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=False),
        sa.Column("horse_number", sa.Integer, nullable=False),
        sa.Column("horse_id", sa.String(255), nullable=False),
        sa.Column("odds_place_min", sa.Float, nullable=False),
        sa.Column("odds_place_max", sa.Float, nullable=False),
    )


def downgrade():
    pass
