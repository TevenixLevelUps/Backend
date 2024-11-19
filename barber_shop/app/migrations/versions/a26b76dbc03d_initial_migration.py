"""Initial migration

Revision ID: a26b76dbc03d
Revises: 6b3fb9422bc7
Create Date: 2024-10-16 19:45:07.788598

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a26b76dbc03d'
down_revision: Union[str, None] = '6b3fb9422bc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('services', 'image')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('services', sa.Column('image', postgresql.BYTEA(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
