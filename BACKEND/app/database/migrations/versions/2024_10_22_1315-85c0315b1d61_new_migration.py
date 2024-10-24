"""new migration

Revision ID: 85c0315b1d61
Revises: d2d240604f1e
Create Date: 2024-10-22 13:15:10.402252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '85c0315b1d61'
down_revision: Union[str, None] = 'd2d240604f1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('barrierdetail', 'barrier_tech_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('barrierdetail', 'match_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('barrierdetail', 'match_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('barrierdetail', 'barrier_tech_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###