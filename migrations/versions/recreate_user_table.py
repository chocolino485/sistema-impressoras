"""recreate user table

Revision ID: recreate_user_table
Revises: fix_password_hash_length
Create Date: 2024-04-30 20:36:01.958149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'recreate_user_table'
down_revision = 'fix_password_hash_length'
branch_labels = None
depends_on = None

def upgrade():
    # Remover a tabela user existente
    op.drop_table('user')
    
    # Recriar a tabela user com o tamanho correto do campo password_hash
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=512), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )

def downgrade():
    # Remover a tabela user
    op.drop_table('user')
    
    # Recriar a tabela user com o tamanho original do campo password_hash
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    ) 