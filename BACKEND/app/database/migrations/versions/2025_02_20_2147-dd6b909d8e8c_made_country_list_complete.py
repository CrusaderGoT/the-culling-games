"""made country list complete

Revision ID: dd6b909d8e8c
Revises: 4f8e2a9c53e4
Create Date: 2025-02-20 21:47:34.236206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dd6b909d8e8c'
down_revision: Union[str, None] = '4f8e2a9c53e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
