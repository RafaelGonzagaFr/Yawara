"""alter servico table

Revision ID: 611654e0c708
Revises: 2b47f6fbb9d8
Create Date: 2025-05-21 08:16:13.902879

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '611654e0c708'
down_revision: Union[str, None] = '2b47f6fbb9d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
