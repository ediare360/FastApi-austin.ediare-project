"""add foreign-key to post table

Revision ID: e44a4b320e2e
Revises: 1eea380b6757
Create Date: 2024-10-03 16:48:35.951549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e44a4b320e2e'
down_revision: Union[str, None] = 'dd545b7683bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))


def downgrade():
    op.drop_column('posts','owner_id')
    pass
