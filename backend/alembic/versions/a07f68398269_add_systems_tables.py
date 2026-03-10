"""add_systems_tables

Revision ID: a07f68398269
Revises: 0071_sibling_roms_fs_name
Create Date: 2026-03-10 19:01:52.491770

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a07f68398269'
down_revision = '0071_sibling_roms_fs_name'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('emulators',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=400), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('file_name', sa.String(length=450), nullable=False),
        sa.Column('file_name_no_tags', sa.String(length=450), nullable=False, server_default=''),
        sa.Column('file_name_no_ext', sa.String(length=450), nullable=False, server_default=''),
        sa.Column('file_extension', sa.String(length=100), nullable=False, server_default=''),
        sa.Column('file_path', sa.String(length=1000), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('path_cover_s', sa.Text(), nullable=True),
        sa.Column('path_cover_l', sa.Text(), nullable=True),
        sa.Column('path_screenshots', sa.JSON(), nullable=True),
        sa.Column('missing_from_fs', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table('builds',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=400), nullable=False),
        sa.Column('slug', sa.String(length=200), nullable=False),
        sa.Column('file_name', sa.String(length=450), nullable=False),
        sa.Column('file_name_no_tags', sa.String(length=450), nullable=False, server_default=''),
        sa.Column('file_name_no_ext', sa.String(length=450), nullable=False, server_default=''),
        sa.Column('file_extension', sa.String(length=100), nullable=False, server_default=''),
        sa.Column('file_path', sa.String(length=1000), nullable=False),
        sa.Column('file_size_bytes', sa.BigInteger(), nullable=False, server_default='0'),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('path_cover_s', sa.Text(), nullable=True),
        sa.Column('path_cover_l', sa.Text(), nullable=True),
        sa.Column('path_screenshots', sa.JSON(), nullable=True),
        sa.Column('missing_from_fs', sa.Boolean(), nullable=False, server_default=sa.text('0')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )

    op.create_table('emulator_platforms',
        sa.Column('emulator_id', sa.Integer(), nullable=False),
        sa.Column('platform_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['emulator_id'], ['emulators.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['platform_id'], ['platforms.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('emulator_id', 'platform_id'),
    )


def downgrade() -> None:
    op.drop_table('emulator_platforms')
    op.drop_table('builds')
    op.drop_table('emulators')
