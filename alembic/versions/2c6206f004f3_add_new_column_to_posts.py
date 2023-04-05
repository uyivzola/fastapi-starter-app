"""Add new column to posts

Revision ID: 2c6206f004f3
Revises: 4de6be464b39
Create Date: 2023-04-05 03:28:02.092665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c6206f004f3'
down_revision = '4de6be464b39'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
