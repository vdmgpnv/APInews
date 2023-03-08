"""add tag field

Revision ID: 682b0aaac4ad
Revises: c24219b64df2
Create Date: 2023-03-08 12:56:58.912903

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '682b0aaac4ad'
down_revision = 'c24219b64df2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('news', sa.Column('tag', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('news', 'tag')
    # ### end Alembic commands ###
