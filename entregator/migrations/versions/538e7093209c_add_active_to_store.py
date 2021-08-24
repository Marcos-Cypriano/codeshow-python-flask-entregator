"""add active to Store

Revision ID: 538e7093209c
Revises: d95ec6e2b6cb
Create Date: 2021-08-18 11:10:22.000897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '538e7093209c'
down_revision = 'd95ec6e2b6cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('store', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('store', 'active')
    # ### end Alembic commands ###
