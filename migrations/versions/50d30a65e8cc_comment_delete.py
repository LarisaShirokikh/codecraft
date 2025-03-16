"""comment delete

Revision ID: 50d30a65e8cc
Revises: e58e7369efae
Create Date: 2025-03-14 20:09:00.412528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50d30a65e8cc'
down_revision: Union[str, None] = 'e58e7369efae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
