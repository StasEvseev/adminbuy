"""empty message

Revision ID: 349f908b69cd
Revises: 2ee0a4b92671
Create Date: 2015-11-17 12:50:13.375520

"""

# revision identifiers, used by Alembic.
revision = '349f908b69cd'
down_revision = '2ee0a4b92671'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('linkacceptanceinvoice',
    sa.Column('acceptance_id', sa.Integer(), nullable=True),
    sa.Column('invoice_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['acceptance_id'], ['acceptance.id'], ),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('linkacceptanceinvoice')
    ### end Alembic commands ###
