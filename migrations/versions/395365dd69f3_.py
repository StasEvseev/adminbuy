"""empty message

Revision ID: 395365dd69f3
Revises: 4d9a2f4596d5
Create Date: 2015-11-17 13:12:41.333885

"""

# revision identifiers, used by Alembic.
revision = '395365dd69f3'
down_revision = '4d9a2f4596d5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'acceptance_invoice_id_key', 'acceptance', type_='unique')
    op.drop_constraint(u'acceptance_waybill_id_key', 'acceptance', type_='unique')
    op.drop_constraint(u'acceptance_waybill_id_fkey', 'acceptance', type_='foreignkey')
    op.drop_constraint(u'acceptance_invoice_id_fkey', 'acceptance', type_='foreignkey')
    op.drop_column(u'acceptance', 'invoice_id')
    op.drop_column(u'acceptance', 'waybill_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'acceptance', sa.Column('waybill_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column(u'acceptance', sa.Column('invoice_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'acceptance_invoice_id_fkey', 'acceptance', 'invoice', ['invoice_id'], ['id'])
    op.create_foreign_key(u'acceptance_waybill_id_fkey', 'acceptance', 'way_bill', ['waybill_id'], ['id'])
    op.create_unique_constraint(u'acceptance_waybill_id_key', 'acceptance', ['waybill_id'])
    op.create_unique_constraint(u'acceptance_invoice_id_key', 'acceptance', ['invoice_id'])
    ### end Alembic commands ###