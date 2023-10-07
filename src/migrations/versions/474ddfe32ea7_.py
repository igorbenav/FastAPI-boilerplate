"""empty message

Revision ID: 474ddfe32ea7
Revises: 211a8b0d0080
Create Date: 2023-10-07 02:22:22.612109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '474ddfe32ea7'
down_revision: Union[str, None] = '211a8b0d0080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post', 'media_url',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_unique_constraint(None, 'post', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='unique')
    op.alter_column('post', 'media_url',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###