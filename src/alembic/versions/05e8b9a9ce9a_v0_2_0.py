"""v0.2.0

Revision ID: 05e8b9a9ce9a
Revises: 
Create Date: 2023-03-30 20:43:45.411480

"""
from alembic import op
import sqlalchemy as sa
import asyncio
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.core.settings import settings
from src.services.secure import SecureService


# revision identifiers, used by Alembic.
revision = '05e8b9a9ce9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    users = op.create_table('users',
        sa.Column('guid', GUID(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password_hashed', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('guid'),
        sa.UniqueConstraint('login')
    )
    op.bulk_insert(users, [{
        'guid': GUID_DEFAULT_SQLITE(),
        'login': settings.admin_login,
        'password_hashed': asyncio.run(SecureService.hash_password(settings.admin_password)),
    }])

    op.create_table('bots',
        sa.Column('guid', GUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('guid')
    )

    op.create_table('relations',
        sa.Column('user_guid', GUID(), nullable=False),
        sa.Column('bot_guid', GUID(), nullable=False),
        sa.ForeignKeyConstraint(['bot_guid'], ['bots.guid'], ),
        sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ),
        sa.PrimaryKeyConstraint('user_guid', 'bot_guid')
    )

    op.create_table('intents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('rank', sa.Integer(), nullable=True),
        sa.Column('bot_guid', GUID(), nullable=False),
        sa.Column('created_by', GUID(), nullable=True),
        sa.ForeignKeyConstraint(['bot_guid'], ['bots.guid'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.guid'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('examples',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('intent_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['intent_id'], ['intents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('admin_chat_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('user_guid', GUID(), nullable=False),
        sa.Column('bot_guid', GUID(), nullable=False),
        sa.Column('intent_rank', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bot_guid'], ['bots.guid'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_guid'], ['users.guid'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('client_chat_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('message', sa.String(), nullable=False),
        sa.Column('in_doubt', sa.Boolean(), nullable=True),
        sa.Column('client_id', sa.String(), nullable=False),
        sa.Column('bot_guid', GUID(), nullable=False),
        sa.Column('intent_rank', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['bot_guid'], ['bots.guid'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('bots')
    op.drop_table('relations')
    op.drop_table('intents')
    op.drop_table('examples')
    op.drop_table('admin_chat_log')
    op.drop_table('client_chat_log')
