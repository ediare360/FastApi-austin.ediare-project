"""relationship

Revision ID: 5d951e45363c
Revises: ed6fec6297ae
Create Date: 2024-10-11 16:33:49.050171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d951e45363c'
down_revision: Union[str, None] = 'ed6fec6297ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name='posts')
    pass
