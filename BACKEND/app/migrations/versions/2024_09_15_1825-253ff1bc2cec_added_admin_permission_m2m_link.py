"""added admin permission m2m link

Revision ID: 253ff1bc2cec
Revises: 7af409ab70d5
Create Date: 2024-09-15 18:25:06.890804

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '253ff1bc2cec'
down_revision: Union[str, None] = '7af409ab70d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adminpermissionlink',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['adminuser.id'], ),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], ),
    sa.PrimaryKeyConstraint('admin_id', 'permission_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('adminpermissionlink')
    # ### end Alembic commands ###