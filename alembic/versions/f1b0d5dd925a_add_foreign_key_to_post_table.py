"""Add foreign key to post table

Revision ID: f1b0d5dd925a
Revises: 3765c37c1ac1
Create Date: 2023-04-05 04:04:59.684680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1b0d5dd925a'
down_revision = '3765c37c1ac1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'], remote_cols=['id'],ondelete='CASCADE')

def downgrade():
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
