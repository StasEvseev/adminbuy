"""empty message

Revision ID: 14cf2440b756
Revises: 31016f83e1b9
Create Date: 2014-10-15 00:28:49.641366

"""

# revision identifiers, used by Alembic.
revision = '14cf2440b756'
down_revision = '31016f83e1b9'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('price',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commodity_id', sa.Integer(), nullable=True),
    sa.Column('number_from', sa.String(length=250), nullable=True),
    sa.Column('NDS', sa.DECIMAL(), nullable=True),
    sa.Column('price_prev', sa.DECIMAL(), nullable=True),
    sa.Column('price_post', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['commodity_id'], ['commodity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'commodity', sa.Column('thematic', sa.String(length=250), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'commodity', 'thematic')
    op.drop_table('price')
    ### end Alembic commands ###
