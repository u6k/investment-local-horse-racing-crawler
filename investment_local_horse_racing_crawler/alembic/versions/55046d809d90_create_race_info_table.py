"""create race_info table

Revision ID: 55046d809d90
Revises:
Create Date: 2020-03-30 06:29:33.985630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55046d809d90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "race_info",
        sa.Column("race_id", sa.String(255), primary_key=True),
        sa.Column("race_round", sa.Integer, nullable=False),
        sa.Column("start_datetime", sa.DateTime, nullable=False),
        sa.Column("place_name", sa.String(255), nullable=False),
        sa.Column("race_name", sa.String(255), nullable=False),
        sa.Column("course_type", sa.String(255), nullable=False),
        sa.Column("course_length", sa.Integer, nullable=False),
        sa.Column("weather", sa.String(255), nullable=False),
        sa.Column("moisture", sa.Float, nullable=False),
        sa.Column("added_money", sa.String(255), nullable=False),
    )

    op.create_table(
        "race_denma",
        sa.Column("race_denma_id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=False),
        sa.Column("bracket_number", sa.Integer, nullable=False),
        sa.Column("horse_number", sa.Integer, nullable=False),
        sa.Column("horse_id", sa.String(100), nullable=False),
        sa.Column("horse_weight", sa.Float, nullable=False),
        sa.Column("horse_weight_diff", sa.Float, nullable=False),
        sa.Column("trainer_id", sa.String(100), nullable=False),
        sa.Column("jockey_id", sa.String(100), nullable=False),
        sa.Column("jockey_weight", sa.Float, nullable=False),
        sa.Column("odds_win", sa.Float, nullable=False),
        sa.Column("favorite", sa.Integer, nullable=False),
    )


def downgrade():
    pass
