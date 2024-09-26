"""added winner_id

Revision ID: 935683e37a47
Revises: 6e40f2c27e78
Create Date: 2024-09-25 13:00:22.390544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '935683e37a47'
down_revision: Union[str, None] = '6e40f2c27e78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('match', sa.Column('winner_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'match', 'player', ['winner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'match', type_='foreignkey')
    op.drop_column('match', 'winner_id')
    # ### end Alembic commands ###
