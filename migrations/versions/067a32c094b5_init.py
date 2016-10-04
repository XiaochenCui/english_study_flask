"""init

Revision ID: 067a32c094b5
Revises: None
Create Date: 2016-10-04 10:56:52.921707

"""

# revision identifiers, used by Alembic.
revision = '067a32c094b5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=64), nullable=True),
                    sa.Column('password_hash', sa.String(length=128), nullable=True),
                    sa.Column('admin', sa.Boolean(), nullable=True),
                    sa.Column('level', sa.String(length=64), nullable=True),
                    sa.Column('words', sa.PickleType(), nullable=True),
                    sa.Column('words_today', sa.PickleType(), nullable=True),
                    sa.Column('words_update_time', sa.DateTime(), nullable=True),
                    sa.Column('task_complied', sa.Boolean(), nullable=True),
                    sa.Column('learn_word_number_every_day', sa.Integer(), nullable=True),
                    sa.Column('last_seen', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('words',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('word', sa.String(length=128), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('phonetic', sa.String(length=128), nullable=True),
                    sa.Column('tags', sa.PickleType(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_words_word'), 'words', ['word'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_words_word'), table_name='words')
    op.drop_table('words')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    ### end Alembic commands ###