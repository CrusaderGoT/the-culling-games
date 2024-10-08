"""test remove column

Revision ID: c993a4835614
Revises: 90edb6c2c688
Create Date: 2024-09-15 16:42:29.020268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c993a4835614'
down_revision: Union[str, None] = '90edb6c2c688'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permission', 'model')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permission', sa.Column('model', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
