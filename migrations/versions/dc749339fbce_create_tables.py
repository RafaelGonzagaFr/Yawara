"""create tables

Revision ID: dc749339fbce
Revises: 19852b161787
Create Date: 2025-05-20 16:05:22.993651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc749339fbce'
down_revision: Union[str, None] = '19852b161787'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
