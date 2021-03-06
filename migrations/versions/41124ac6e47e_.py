"""empty message

Revision ID: 41124ac6e47e
Revises: 57296b50c499
Create Date: 2014-11-30 17:08:44.396000

"""

# revision identifiers, used by Alembic.
revision = '41124ac6e47e'
down_revision = '57296b50c499'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('provider', sa.Column('address', sa.String(length=250), nullable=True))
    op.add_column('provider', sa.Column('emails', sa.String(length=250), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('provider', 'emails')
    op.drop_column('provider', 'address')
    ### end Alembic commands ###
