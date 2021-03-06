"""empty message

Revision ID: b62a0c2c8edf
Revises: 819ee7205099
Create Date: 2021-11-04 09:48:17.752536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b62a0c2c8edf'
down_revision = '819ee7205099'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_checkout_created_at'), 'checkout', ['created_at'], unique=False)
    op.create_index(op.f('ix_order_created_at'), 'order', ['created_at'], unique=False)
    op.create_unique_constraint(None, 'store', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'store', type_='unique')
    op.drop_index(op.f('ix_order_created_at'), table_name='order')
    op.drop_index(op.f('ix_checkout_created_at'), table_name='checkout')
    # ### end Alembic commands ###
