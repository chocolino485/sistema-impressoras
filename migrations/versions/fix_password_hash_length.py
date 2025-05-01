"""fix password hash length

Revision ID: fix_password_hash_length
Revises: c021f727c2ed
Create Date: 2024-04-30 20:36:01.958149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fix_password_hash_length'
down_revision = 'c021f727c2ed'
branch_labels = None
depends_on = None

def upgrade():
    # Alterar o tipo da coluna password_hash para String(512)
    op.alter_column('user', 'password_hash',
                    existing_type=sa.String(length=128),
                    type_=sa.String(length=512),
                    existing_nullable=True)

def downgrade():
    # Reverter a alteração para String(128)
    op.alter_column('user', 'password_hash',
                    existing_type=sa.String(length=512),
                    type_=sa.String(length=128),
                    existing_nullable=True) 