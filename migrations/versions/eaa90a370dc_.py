"""empty message

Revision ID: eaa90a370dc
Revises: 26c14dc2ce0b
Create Date: 2015-03-31 10:59:47.040222

"""

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

revision = 'eaa90a370dc'
down_revision = '26c14dc2ce0b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('acceptance', sa.Column('provider_id', sa.Integer(), nullable=True))
    bind = op.get_bind()
    if type(bind.dialect) == SQLiteDialect_pysqlite:
        try:
            op.create_foreign_key(None, 'acceptance', 'provider', ['provider_id'], ['id'])
        except Exception as exc:
            pass
    else:
        op.create_foreign_key(None, 'acceptance', 'provider', ['provider_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'acceptance', type_='foreignkey')
    op.drop_column('acceptance', 'provider_id')
    ### end Alembic commands ###
