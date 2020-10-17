"""init

Revision ID: 7491ceeb5053
Revises: 
Create Date: 2020-10-16 23:46:04.219483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7491ceeb5053'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "calendar_race_url",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("calendar_url", sa.String(255), nullable=False),
        sa.Column("race_list_url", sa.String(255), nullable=False),
    )

    op.create_table(
        "race_info_mini",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_list_url", sa.String(255), nullable=False),
        sa.Column("race_name", sa.String(255), nullable=True),
        sa.Column("race_denma_url", sa.String(255), nullable=True),
        sa.Column("course_length", sa.String(255), nullable=True),
        sa.Column("start_time", sa.String(255), nullable=True),
    )

    op.create_table(
        "race_info",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_denma_url", sa.String(255), nullable=False),
        sa.Column("race_round", sa.String(255), nullable=True),
        sa.Column("race_name", sa.String(255), nullable=True),
        sa.Column("start_date", sa.String(255), nullable=True),
        sa.Column("place_name", sa.String(255), nullable=True),
        sa.Column("course_type_length", sa.String(255), nullable=True),
        sa.Column("start_time", sa.String(255), nullable=True),
        sa.Column("weather_url", sa.String(255), nullable=True),
        sa.Column("course_condition", sa.String(255), nullable=True),
        sa.Column("moisture", sa.String(255), nullable=True),
        sa.Column("prize_money", sa.String(255), nullable=True),
    )

    op.create_table(
        "race_denma",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_denma_url", sa.String(255), nullable=False),
        sa.Column("bracket_number", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("horse_url", sa.String(255), nullable=True),
        sa.Column("jockey_url", sa.String(255), nullable=True),
        sa.Column("jockey_weight", sa.String(255), nullable=True),
        sa.Column("trainer_url", sa.String(255), nullable=True),
        sa.Column("odds_win_favorite", sa.String(255), nullable=True),
        sa.Column("horse_weight", sa.String(255), nullable=True),
        sa.Column("horse_weight_diff", sa.String(255), nullable=True),
    )



def downgrade():
    pass
