"""Add created_at column

Revision ID: e41156ab6f8b
Revises: 2c6206f004f3
Create Date: 2023-04-05 03:36:54.358334

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision = 'e41156ab6f8b'
down_revision = '2c6206f004f3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()')))
    


def downgrade():
    op.drop_column('posts', 'created_at')
    
