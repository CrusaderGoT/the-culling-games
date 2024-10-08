"""removed cascade of player if user is deleted

Revision ID: 0ef30d1d3aa3
Revises: fa281adbd7dd
Create Date: 2024-09-25 13:34:28.302994

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0ef30d1d3aa3'
down_revision: Union[str, None] = 'fa281adbd7dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('player_user_id_fkey', 'player', type_='foreignkey')
    op.drop_constraint('player_colony_id_fkey', 'player', type_='foreignkey')
    op.drop_constraint('player_ct_id_fkey', 'player', type_='foreignkey')
    op.create_foreign_key(None, 'player', 'user', ['user_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'player', 'cursedtechnique', ['ct_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'player', 'colony', ['colony_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'player', type_='foreignkey')
    op.drop_constraint(None, 'player', type_='foreignkey')
    op.drop_constraint(None, 'player', type_='foreignkey')
    op.create_foreign_key('player_ct_id_fkey', 'player', 'cursedtechnique', ['ct_id'], ['id'])
    op.create_foreign_key('player_colony_id_fkey', 'player', 'colony', ['colony_id'], ['id'])
    op.create_foreign_key('player_user_id_fkey', 'player', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
