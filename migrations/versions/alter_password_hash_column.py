"""alter password hash column

Revision ID: alter_password_hash_column
Revises: recreate_user_table
Create Date: 2024-04-30 20:36:01.958149

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'alter_password_hash_column'
down_revision = 'recreate_user_table'
branch_labels = None
depends_on = None

def upgrade():
    # Usando SQL nativo do PostgreSQL para alterar o tipo da coluna
    op.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(512)')

def downgrade():
    # Reverter para VARCHAR(128)
    op.execute('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(128)') 