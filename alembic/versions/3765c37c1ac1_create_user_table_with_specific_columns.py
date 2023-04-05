"""Create user table with specific columns

Revision ID: 3765c37c1ac1
Revises: e41156ab6f8b
Create Date: 2023-04-05 03:54:54.487624

"""
import sqlalchemy as sa
from sqlalchemy.sql.expression import text

from alembic import op

# revision identifiers, used by Alembic.
revision = '3765c37c1ac1'
down_revision = 'e41156ab6f8b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, index=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
