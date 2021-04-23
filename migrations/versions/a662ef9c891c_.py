"""empty message

Revision ID: a662ef9c891c
Revises: 5a102a17176a
Create Date: 2021-04-08 22:06:16.750808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a662ef9c891c'
down_revision = '5a102a17176a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('color', sa.String(length=200), nullable=True),
    sa.Column('type', sa.Enum('NAZI', 'LIBERAL', 'POPULIST', 'COMMUNIST', 'CONSERVATIVES', 'SOCIALISTS', 'NATIONALISTS', 'DEMOCRATS', name='partyenum'), nullable=True),
    sa.Column('founded_at', sa.Date(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parties')
    # ### end Alembic commands ###
