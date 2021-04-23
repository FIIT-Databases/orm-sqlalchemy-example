"""empty message

Revision ID: 264d806b2387
Revises: 8502091fc2e2
Create Date: 2021-04-08 22:32:58.482017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '264d806b2387'
down_revision = '8502091fc2e2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parties', 'founded_at',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('parties', 'founded_at',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
