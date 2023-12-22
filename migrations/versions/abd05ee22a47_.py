"""empty message

Revision ID: abd05ee22a47
Revises: 306e8314f7ab
Create Date: 2023-03-27 14:12:01.773802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'abd05ee22a47'
down_revision = '306e8314f7ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.drop_column('statuss')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('employee', schema=None) as batch_op:
        batch_op.add_column(sa.Column('statuss', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
