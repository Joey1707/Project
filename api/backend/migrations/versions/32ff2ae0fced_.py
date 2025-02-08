"""empty message

Revision ID: 32ff2ae0fced
Revises: 46a436be4d0a
Create Date: 2025-01-28 11:21:53.862128

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '32ff2ae0fced'
down_revision = '46a436be4d0a'
branch_labels = None
depends_on = None


def upgrade():
    # Rename the column 'name' to 'username'
    op.alter_column('userdata', 'name', new_column_name='username')

    # Drop the index on the 'email' column
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.drop_index('email')


def downgrade():
    # Rename the column 'username' back to 'name'
    op.alter_column('userdata', 'username', new_column_name='name')

    # Recreate the index on the 'email' column
    with op.batch_alter_table('userdata', schema=None) as batch_op:
        batch_op.create_index('email', ['email'], unique=True)

