"""add user.last_seen

Revision ID: 7b5df128884d
Revises: ec0c8ee30d4f
Create Date: 2016-10-01 21:46:44.220752

"""

# revision identifiers, used by Alembic.
revision = '7b5df128884d'
down_revision = 'ec0c8ee30d4f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('lask_seen', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lask_seen')
    ### end Alembic commands ###