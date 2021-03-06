"""add on_menu to Category

Revision ID: d95ec6e2b6cb
Revises: 
Create Date: 2021-08-18 11:02:42.108143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd95ec6e2b6cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('on_menu', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'on_menu')
    # ### end Alembic commands ###
