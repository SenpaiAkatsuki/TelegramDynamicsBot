"""seed items

Revision ID: c717ca3b1850
Revises: 964c5db6eb96
Create Date: 2023-02-07 03:48:23.800140

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'c717ca3b1850'
down_revision = '964c5db6eb96'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scheduled_messages', sa.Column('next_send_time', sa.TIMESTAMP(), nullable=True))
    meta = sa.MetaData()
    meta.reflect(bind=op.get_bind(), only=['groups'])
    groups_table = sa.Table('groups', meta)
    op.bulk_insert(
        groups_table,
        [
            {'name': 'Group 1', 'group_id': -1003123213221},
            {'name': 'Group 2', 'group_id': -1003123213222},
            {'name': 'Group 3', 'group_id': -1003123213223},
            {'name': 'Group 4', 'group_id': -1003123213224},
        ]
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scheduled_messages', 'next_send_time')
    op.execute(text('DELETE FROM groups'))
    # ### end Alembic commands ###
