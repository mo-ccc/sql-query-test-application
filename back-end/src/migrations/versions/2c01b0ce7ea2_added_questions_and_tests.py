"""added questions and tests

Revision ID: 2c01b0ce7ea2
Revises: 226588e2564b
Create Date: 2021-04-13 20:05:31.220470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c01b0ce7ea2'
down_revision = '226588e2564b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('prompt', sa.String(), nullable=False),
    sa.Column('answer_as_query', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('time_started', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('time_submitted', sa.DateTime(), nullable=True),
    sa.Column('user_submitted_query', sa.String(), nullable=True),
    sa.Column('result', sa.SmallInteger(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tests')
    op.drop_table('questions')
    # ### end Alembic commands ###
