"""cascade update and delete

Revision ID: 14b1232262a3
Revises: aa8e3bfd7f10
Create Date: 2023-04-04 10:52:05.190095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14b1232262a3'
down_revision = 'aa8e3bfd7f10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('admin_chat_log_bot_guid_fkey',
                       'admin_chat_log', type_='foreignkey')
    op.create_foreign_key('fk_admin_chat_log__bot_guid', 'admin_chat_log', 'bots', [
                          'bot_guid'], ['guid'], onupdate='CASCADE', ondelete='CASCADE')

    op.drop_constraint('client_chat_log_bot_guid_fkey',
                       'client_chat_log', type_='foreignkey')
    op.create_foreign_key('fk_client_chat_log__bot_guid', 'client_chat_log', 'bots', [
                          'bot_guid'], ['guid'], onupdate='CASCADE', ondelete='CASCADE')

    op.drop_constraint('examples_intent_id_fkey',
                       'examples', type_='foreignkey')
    op.create_foreign_key('fk_examples__intent_id', 'examples', 'intents', [
                          'intent_id'], ['id'], ondelete='CASCADE')

    op.drop_constraint('intents_bot_guid_fkey', 'intents', type_='foreignkey')
    op.create_foreign_key('fk_intents__bot_guid', 'intents', 'bots', ['bot_guid'], [
                          'guid'], onupdate='CASCADE', ondelete='CASCADE')

    op.drop_constraint('relations_user_guid_fkey',
                       'relations', type_='foreignkey')
    op.drop_constraint('relations_bot_guid_fkey',
                       'relations', type_='foreignkey')

    op.create_foreign_key('fk_relations__user_guid', 'relations', 'users', [
                          'user_guid'], ['guid'], ondelete='CASCADE')
    op.create_foreign_key('fk_relations__bot_guid', 'relations', 'bots', [
                          'bot_guid'], ['guid'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('fk_relations__bot_guid',
                       'relations', type_='foreignkey')
    op.drop_constraint('fk_relations__user_guid',
                       'relations', type_='foreignkey')
    op.create_foreign_key('relations_bot_guid_fkey',
                          'relations', 'bots', ['bot_guid'], ['guid'])
    op.create_foreign_key('relations_user_guid_fkey',
                          'relations', 'users', ['user_guid'], ['guid'])

    op.drop_constraint('fk_intents__bot_guid', 'intents', type_='foreignkey')
    op.create_foreign_key('intents_bot_guid_fkey',
                          'intents', 'bots', ['bot_guid'], ['guid'])

    op.drop_constraint('fk_examples__intent_id',
                       'examples', type_='foreignkey')
    op.create_foreign_key('examples_intent_id_fkey',
                          'examples', 'intents', ['intent_id'], ['id'])

    op.drop_constraint('fk_client_chat_log__bot_guid',
                       'client_chat_log', type_='foreignkey')
    op.create_foreign_key('client_chat_log_bot_guid_fkey', 'client_chat_log', 'bots', [
                          'bot_guid'], ['guid'], ondelete='CASCADE')

    op.drop_constraint('fk_admin_chat_log__bot_guid',
                       'admin_chat_log', type_='foreignkey')
    op.create_foreign_key('admin_chat_log_bot_guid_fkey', 'admin_chat_log', 'bots', [
                          'bot_guid'], ['guid'], ondelete='CASCADE')
