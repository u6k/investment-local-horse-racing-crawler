"""alter column horse owner nullable

Revision ID: db6db4289e1b
Revises: 875f40acd9b4
Create Date: 2020-04-02 16:38:05.469578

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'db6db4289e1b'
down_revision = '875f40acd9b4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("horse", "owner", nullable=True)


def downgrade():
    pass
