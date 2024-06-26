"""add unique to group_id

Revision ID: 1ee299f599de
Revises: 98fa205df747
Create Date: 2023-02-25 13:45:56.569903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ee299f599de'
down_revision = '98fa205df747'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'group_settings', ['group_id'])
    op.alter_column('messages', 'template_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'scheduled_messages', 'templates', ['template_id'], ['template_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scheduled_messages', type_='foreignkey')
    op.alter_column('messages', 'template_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint(None, 'group_settings', type_='unique')
    # ### end Alembic commands ###
