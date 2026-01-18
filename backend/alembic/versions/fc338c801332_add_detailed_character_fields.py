"""Add detailed character fields

Revision ID: fc338c801332
Revises: 
Create Date: 2026-01-18 16:50:54.397445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc338c801332'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to characters table
    op.add_column('characters', sa.Column('saving_throws', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('skills', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('armor_class', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('initiative', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('speed', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('hit_points_max', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('hit_points_current', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('hit_points_temp', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('hit_dice', sa.String(), nullable=True))
    op.add_column('characters', sa.Column('proficiencies', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('languages', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('features', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('traits', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('spells', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('spell_slots', sa.JSON(), nullable=True))
    op.add_column('characters', sa.Column('spellcasting_ability', sa.String(), nullable=True))
    op.add_column('characters', sa.Column('spell_save_dc', sa.Integer(), nullable=True))
    op.add_column('characters', sa.Column('spell_attack_bonus', sa.Integer(), nullable=True))


def downgrade() -> None:
    # Remove columns in reverse order
    op.drop_column('characters', 'spell_attack_bonus')
    op.drop_column('characters', 'spell_save_dc')
    op.drop_column('characters', 'spellcasting_ability')
    op.drop_column('characters', 'spell_slots')
    op.drop_column('characters', 'spells')
    op.drop_column('characters', 'traits')
    op.drop_column('characters', 'features')
    op.drop_column('characters', 'languages')
    op.drop_column('characters', 'proficiencies')
    op.drop_column('characters', 'hit_dice')
    op.drop_column('characters', 'hit_points_temp')
    op.drop_column('characters', 'hit_points_current')
    op.drop_column('characters', 'hit_points_max')
    op.drop_column('characters', 'speed')
    op.drop_column('characters', 'initiative')
    op.drop_column('characters', 'armor_class')
    op.drop_column('characters', 'skills')
    op.drop_column('characters', 'saving_throws')
