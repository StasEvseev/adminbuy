"""empty message

Revision ID: 3ba659b6b340
Revises: 40c090cb04b6
Create Date: 2015-09-12 00:06:39.102000

"""

# revision identifiers, used by Alembic.
revision = '3ba659b6b340'
down_revision = '40c090cb04b6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    ### end Alembic commands ###
