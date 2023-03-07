"""create unique constraint

Revision ID: c24219b64df2
Revises: af243044ecf3
Create Date: 2023-03-07 22:39:51.424276

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c24219b64df2'
down_revision = 'af243044ecf3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('news_unique', 'news', ['publication_date', 'header'], schema='public')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('news_unique', 'news', schema='public', type_='unique')
    # ### end Alembic commands ###