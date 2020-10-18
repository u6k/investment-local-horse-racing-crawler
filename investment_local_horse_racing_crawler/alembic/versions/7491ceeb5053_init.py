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
    
    op.create_table(
        "race_result",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_result_url", sa.String(255), nullable=False),
        sa.Column("result", sa.String(255), nullable=True),
        sa.Column("bracket_number", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("horse_url", sa.String(255), nullable=False),
        sa.Column("arrival_time", sa.String(255), nullable=True),
        sa.Column("arrival_margin", sa.String(255), nullable=True),
        sa.Column("final_600_meters_time", sa.String(255), nullable=True),
        sa.Column("corner_passing_order", sa.String(255), nullable=True),
    )
    
    op.create_table(
        "race_corner_passing_order",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_result_url", sa.String(255), nullable=False),
        sa.Column("corner_number", sa.String(255), nullable=True),
        sa.Column("passing_order", sa.String(255), nullable=True),
    )
    
    op.create_table(
        "race_refund",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("race_result_url", sa.String(255), nullable=False),
        sa.Column("betting_type", sa.String(255), nullable=True),
        sa.Column("horse_number", sa.String(255), nullable=True),
        sa.Column("refund_money", sa.String(255), nullable=True),
        sa.Column("favorite", sa.String(255), nullable=True),
    )
    
    op.create_table(
        "horse",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("horse_url", sa.String(255), nullable=False),
        sa.Column("horse_name", sa.String(255), nullable=True),
        sa.Column("gender_age", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("coat_color", sa.String(255), nullable=True),
        sa.Column("trainer_url", sa.String(255), nullable=True),
        sa.Column("owner", sa.String(255), nullable=True),
        sa.Column("breeder", sa.String(255), nullable=True),
        sa.Column("breeding_farm", sa.String(255), nullable=True),
        sa.Column("parent_horse_name_1", sa.String(255), nullable=True),
        sa.Column("parent_horse_name_2", sa.String(255), nullable=True),
        sa.Column("grand_parent_horse_name_1", sa.String(255), nullable=True),
        sa.Column("grand_parent_horse_name_2", sa.String(255), nullable=True),
        sa.Column("grand_parent_horse_name_3", sa.String(255), nullable=True),
        sa.Column("grand_parent_horse_name_4", sa.String(255), nullable=True),
    )
    
    op.create_table(
        "jockey",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("jockey_url", sa.String(255), nullable=False),
        sa.Column("jockey_name", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("gender", sa.String(255), nullable=True),
        sa.Column("belong_to", sa.String(255), nullable=True),
        sa.Column("trainer_url", sa.String(255), nullable=True),
        sa.Column("first_licensing_year", sa.String(255), nullable=True),
    )
    
    op.create_table(
        "trainer",
        sa.Column("id", sa.String(255), primary_key=True),
        sa.Column("trainer_url", sa.String(255), nullable=False),
        sa.Column("trainer_name", sa.String(255), nullable=True),
        sa.Column("birthday", sa.String(255), nullable=True),
        sa.Column("gender", sa.String(255), nullable=True),
        sa.Column("belong_to", sa.String(255), nullable=True),
    )



def downgrade():
    pass
