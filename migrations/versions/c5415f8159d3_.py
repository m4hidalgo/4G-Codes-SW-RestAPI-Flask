"""empty message

Revision ID: c5415f8159d3
Revises: b9b28c9dcacf
Create Date: 2022-11-26 12:53:09.147956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5415f8159d3'
down_revision = 'b9b28c9dcacf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Favorites', schema=None) as batch_op:
        batch_op.drop_constraint('Favorites_people_id_key', type_='unique')
        batch_op.drop_constraint('Favorites_planet_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Favorites', schema=None) as batch_op:
        batch_op.create_unique_constraint('Favorites_planet_id_key', ['planet_id'])
        batch_op.create_unique_constraint('Favorites_people_id_key', ['people_id'])

    # ### end Alembic commands ###