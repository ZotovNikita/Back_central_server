"""add users, bots, roles, relations

Revision ID: b79b89418572
Revises: 
Create Date: 2023-02-20 20:59:06.087050

"""
from alembic import op
import sqlalchemy as sa
from src.utils.guid import GUID


# revision identifiers, used by Alembic.
revision = 'b79b89418572'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bots',
    sa.Column('guid', GUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('model_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_table('roles',
    sa.Column('guid', GUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_table('users',
    sa.Column('guid', GUID(), nullable=False),
    sa.Column('login', sa.String(), nullable=False),
    sa.Column('password_hashed', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('guid'),
    sa.UniqueConstraint('login')
    )
    op.create_table('relations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_guid', GUID(), nullable=False),
    sa.Column('bot_guid', GUID(), nullable=False),
    sa.Column('role_guid', GUID(), nullable=False),
    sa.ForeignKeyConstraint(['bot_guid'], ['bots.guid'], ),
    sa.ForeignKeyConstraint(['role_guid'], ['roles.guid'], ),
    sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relations')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('bots')
    # ### end Alembic commands ###
