"""Added expired in Order table

Revision ID: 819ee7205099
Revises: 538e7093209c
Create Date: 2021-10-13 07:34:50.630526

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '819ee7205099'
down_revision = '538e7093209c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('expired', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('order', 'expired')
    # ### end Alembic commands ###
