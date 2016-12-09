"""empty message

Revision ID: 57296b50c499
Revises: 223a10a61da8
Create Date: 2014-11-17 14:43:39.309104

"""

# revision identifiers, used by Alembic.
revision = '57296b50c499'
down_revision = '223a10a61da8'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice_item', sa.Column('good_id', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice_item', 'good_id')
    ### end Alembic commands ###