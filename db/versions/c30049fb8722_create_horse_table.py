"""create horse table

Revision ID: c30049fb8722
Revises: 7e3a81741029
Create Date: 2020-04-01 08:35:32.542618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c30049fb8722'
down_revision = '7e3a81741029'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "horse",
        sa.Column("horse_id", sa.String(255), primary_key=True),
        sa.Column("horse_name", sa.String(255), nullable=False),
        sa.Column("gender", sa.String(255), nullable=False),
        sa.Column("age", sa.Integer, nullable=False),
        sa.Column("birthday", sa.DateTime, nullable=False),
        sa.Column("coat_color", sa.String(255), nullable=False),
        sa.Column("owner", sa.String(255), nullable=False),
        sa.Column("breeder", sa.String(255), nullable=False),
        sa.Column("breeding_farm", sa.String(255), nullable=False),
        sa.Column("parent_horse_name_1", sa.String(255), nullable=False),
        sa.Column("parent_horse_name_2", sa.String(255), nullable=False),
        sa.Column("grand_parent_horse_name_1", sa.String(255), nullable=False),
        sa.Column("grand_parent_horse_name_2", sa.String(255), nullable=False),
        sa.Column("grand_parent_horse_name_3", sa.String(255), nullable=False),
        sa.Column("grand_parent_horse_name_4", sa.String(255), nullable=False),
    )


def downgrade():
    pass
