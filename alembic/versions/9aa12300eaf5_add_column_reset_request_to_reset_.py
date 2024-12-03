"""add column reset_request to reset password logic

Revision ID: 9aa12300eaf5
Revises: 81a0dcca08b1
Create Date: 2024-12-03 16:26:26.680857

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9aa12300eaf5"
down_revision: Union[str, None] = "81a0dcca08b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add the column as nullable initially
    op.add_column("user", sa.Column("reset_requests", sa.Boolean(), nullable=True))

    # Set default value for existing rows
    op.execute('UPDATE "user" SET reset_requests = FALSE WHERE reset_requests IS NULL')

    # Make the column non-nullable
    op.alter_column("user", "reset_requests", nullable=False)


def downgrade() -> None:
    # Remove the column in downgrade
    op.drop_column("user", "reset_requests")
