"""create race_result_payoff table

Revision ID: 7e3a81741029
Revises: 27099e810beb
Create Date: 2020-03-31 03:59:58.739850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e3a81741029'
down_revision = '27099e810beb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "race_result",
        sa.Column("race_result_id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=False),
        sa.Column("bracket_number", sa.Integer, nullable=False),
        sa.Column("horse_number", sa.Integer, nullable=False),
        sa.Column("horse_id", sa.String(255), nullable=False),
        sa.Column("result", sa.Integer, nullable=False),
        sa.Column("arrival_time", sa.Float, nullable=False),
    )

    op.create_table(
        "race_payoff",
        sa.Column("race_payoff_id", sa.String(255), primary_key=True),
        sa.Column("race_id", sa.String(255), nullable=False),
        sa.Column("payoff_type", sa.String(100), nullable=False),
        sa.Column("horse_number_1", sa.Integer, nullable=False),
        sa.Column("horse_number_2", sa.Integer, nullable=True),
        sa.Column("horse_number_3", sa.Integer, nullable=True),
        sa.Column("odds", sa.Float, nullable=False),
        sa.Column("favorite", sa.Integer, nullable=False),
    )


def downgrade():
    pass
