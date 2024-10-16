"""add column to post table

Revision ID: dd545b7683bc
Revises: 531b2f21d4b5
Create Date: 2024-10-03 12:49:11.310145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd545b7683bc'
down_revision: Union[str, None] = '531b2f21d4b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
