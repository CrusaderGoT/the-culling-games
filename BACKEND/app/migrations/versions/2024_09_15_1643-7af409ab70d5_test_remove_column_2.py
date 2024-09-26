"""test remove column 2

Revision ID: 7af409ab70d5
Revises: c993a4835614
Create Date: 2024-09-15 16:43:35.080745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '7af409ab70d5'
down_revision: Union[str, None] = 'c993a4835614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permission', sa.Column('model', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permission', 'model')
    # ### end Alembic commands ###