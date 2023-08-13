"""2

Revision ID: 5bb6c0a8087a
Revises: 
Create Date: 2023-08-13 14:55:29.492213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bb6c0a8087a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('birthdate', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('github', sa.String(), nullable=False),
    sa.Column('education', sa.String(), nullable=True),
    sa.Column('additional_education', sa.String(), nullable=True),
    sa.Column('skills', sa.String(), nullable=False),
    sa.Column('projects', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resume')
    # ### end Alembic commands ###