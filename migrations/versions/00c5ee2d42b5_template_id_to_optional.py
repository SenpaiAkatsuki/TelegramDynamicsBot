"""template_id_to_optional

Revision ID: 00c5ee2d42b5
Revises: b5056cc0a18a
Create Date: 2023-02-23 04:40:44.822748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00c5ee2d42b5'
down_revision = 'b5056cc0a18a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'template_id', existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'template_id', existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###