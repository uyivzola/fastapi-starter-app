"""Create posts table

Revision ID: 4de6be464b39
Revises: 
Create Date: 2023-04-05 03:14:58.429784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4de6be464b39'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,primary_key=True),sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
