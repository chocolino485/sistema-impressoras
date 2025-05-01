"""change password hash to text

Revision ID: change_password_hash_to_text
Revises: alter_password_hash_column
Create Date: 2024-04-30 20:36:01.958149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'change_password_hash_to_text'
down_revision = 'alter_password_hash_column'
branch_labels = None
depends_on = None

def upgrade():
    # Usando SQL nativo do PostgreSQL para alterar o tipo da coluna para TEXT
    op.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE TEXT')

def downgrade():
    # Reverter para VARCHAR(512)
    op.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(512)') 