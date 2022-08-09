"""New

Revision ID: 4d6e9bca4b81
Revises: c1ece687bbda
Create Date: 2022-07-19 12:04:44.657357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d6e9bca4b81'
down_revision = 'c1ece687bbda'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('creation_date', sa.DATE(), nullable=True))
    op.add_column('users', sa.Column('balance', sa.Integer(), nullable=True))
    op.drop_column('users', 'reg_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('reg_date', sa.DATE(), autoincrement=False, nullable=True))
    op.drop_column('users', 'balance')
    op.drop_column('users', 'creation_date')
    # ### end Alembic commands ###
