"""add table users

Revision ID: d6fc570ad0f6
Revises: 
Create Date: 2024-12-27 18:03:17.969097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6fc570ad0f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('Username', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=50), nullable=True),
        sa.Column('password', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('users')
