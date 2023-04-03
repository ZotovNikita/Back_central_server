"""fix chat log

Revision ID: aa8e3bfd7f10
Revises: 05e8b9a9ce9a
Create Date: 2023-04-03 23:13:37.977352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa8e3bfd7f10'
down_revision = '05e8b9a9ce9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('admin_chat_log', sa.Column('answer', sa.String(), nullable=False))
    op.alter_column('admin_chat_log', 'intent_rank',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('client_chat_log', sa.Column('answer', sa.String(), nullable=False))
    op.alter_column('client_chat_log', 'intent_rank',
               existing_type=sa.INTEGER(),
               nullable=False)


def downgrade() -> None:
    op.alter_column('client_chat_log', 'intent_rank',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('client_chat_log', 'answer')
    op.alter_column('admin_chat_log', 'intent_rank',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('admin_chat_log', 'answer')
