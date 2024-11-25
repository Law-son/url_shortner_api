"""removed sqlalchemy instance from models

Revision ID: 9456b5c9c7ae
Revises: 
Create Date: 2024-11-25 11:14:45.764455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9456b5c9c7ae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('url',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('original_url', sa.String(length=2048), nullable=False),
    sa.Column('short_url', sa.String(length=10), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('short_url')
    )
    op.create_table('visit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_agent', sa.String(length=256), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['url_id'], ['url.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('url')
    op.drop_table('user')
    # ### end Alembic commands ###