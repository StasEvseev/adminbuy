"""empty message

Revision ID: 46170ac4b436
Revises: 140ce94a8336
Create Date: 2015-03-30 09:43:08.626966

"""

# revision identifiers, used by Alembic.
revision = '46170ac4b436'
down_revision = '140ce94a8336'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('point_sale', sa.Column('is_central', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('point_sale', 'is_central')
    ### end Alembic commands ###
