"""initial migration

Revision ID: 9fd7969e60d3
Revises: 
Create Date: 2024-09-15 14:03:00.121614

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9fd7969e60d3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('min_amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('min_active_user', sa.BigInteger(), nullable=False),
    sa.Column('rate', sa.Numeric(precision=5, scale=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('code', sa.String(length=40), nullable=False),
    sa.Column('referrer_id', sa.Integer(), nullable=True),
    sa.Column('register_date', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['referrer_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('username')
    )
    op.create_table('investment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=10, scale=5), nullable=False),
    sa.Column('confirm', sa.Boolean(), nullable=False),
    sa.Column('confirm_check_date', sa.DateTime(), nullable=True),
    sa.Column('profit', sa.DECIMAL(precision=10, scale=5), nullable=True),
    sa.Column('last_profit_date', sa.DateTime(), nullable=True),
    sa.Column('request_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('investment')
    op.drop_table('user')
    op.drop_table('rate')
    # ### end Alembic commands ###
