"""Initial

Revision ID: 2c9b979bba8d
Revises: 
Create Date: 2019-06-01 04:29:55.084780+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c9b979bba8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_authors')),
    sa.UniqueConstraint('name', name=op.f('uq_authors_name')),
    sa.UniqueConstraint('slug', name=op.f('uq_authors_slug'))
    )
    op.create_table('books',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('slug', sa.String(length=256), nullable=True),
    sa.Column('author_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], name=op.f('fk_books_author_id_authors')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_books')),
    sa.UniqueConstraint('name', name=op.f('uq_books_name')),
    sa.UniqueConstraint('slug', name=op.f('uq_books_slug'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###