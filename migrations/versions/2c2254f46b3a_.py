"""empty message

Revision ID: 2c2254f46b3a
Revises: 40abc5e3e07
Create Date: 2015-04-09 14:52:43.605602

"""

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.sqlite.pysqlite import SQLiteDialect_pysqlite

revision = '2c2254f46b3a'
down_revision = '40abc5e3e07'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mails', sa.Column('provider_id', sa.Integer(), nullable=True))
    bind = op.get_bind()
    if type(bind.dialect) == SQLiteDialect_pysqlite:
        try:
            op.create_foreign_key(None, 'mails', 'provider', ['provider_id'], ['id'])
        except Exception as exc:
            pass
    else:
        op.create_foreign_key(None, 'mails', 'provider', ['provider_id'], ['id'])

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'mails', type_='foreignkey')
    op.drop_column('mails', 'provider_id')
    ### end Alembic commands ###
