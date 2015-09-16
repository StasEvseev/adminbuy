"""empty message

Revision ID: 4f55a3c62dc6
Revises: 3ba659b6b340
Create Date: 2015-09-16 18:15:07.324821

"""

# revision identifiers, used by Alembic.
revision = '4f55a3c62dc6'
down_revision = '3ba659b6b340'

from alembic import op
from flask_sqlalchemy import _SessionSignalEvents
import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as BaseSession, relationship, backref

Session = sessionmaker()

# event.remove(BaseSession, 'before_commit', _SessionSignalEvents.session_signal_before_commit)
# event.remove(BaseSession, 'after_commit', _SessionSignalEvents.session_signal_after_commit)
# event.remove(BaseSession, 'after_rollback', _SessionSignalEvents.session_signal_after_rollback)

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'
    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))


class RU(Base):
    __tablename__ = 'roles_users'
    user_id = sa.Column(sa.Integer(), sa.ForeignKey('user.id'), primary_key=True)
    role_id = sa.Column(sa.Integer(), sa.ForeignKey('role.id'), primary_key=True)
    role = relationship('Role')


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(100))
    last_name = sa.Column(sa.String(100))
    login = sa.Column(sa.String(80), unique=True, nullable=False)
    email = sa.Column(sa.String(120))
    password = sa.Column(sa.String)
    is_superuser = sa.Column(sa.Boolean, default=False)
    roles = relationship('RU')
    active = sa.Column(sa.Boolean, nullable=True)


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)

    role = Role(name="admin")

    session.add(role)

    admin = session.query(User).filter(User.is_superuser==True).one()

    ru = RU()
    ru.user = admin
    ru.role = role
    admin.roles.append(ru)
    session.add(admin)

    session.commit()
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    pass
    ### end Alembic commands ###
