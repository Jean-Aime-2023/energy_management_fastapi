"""Your migration message

Revision ID: 48363a45d618
Revises: ce280f7837ad
Create Date: 2024-11-29 11:21:42.144375

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '48363a45d618'
down_revision: Union[str, None] = 'ce280f7837ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('energy_consumptions', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('time', sa.Time(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('consumption', sa.Float(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('cost', sa.Float(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('source', sa.String(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('location', sa.String(), nullable=False))
    op.add_column('energy_consumptions', sa.Column('remarks', sa.Text(), nullable=True))
    op.create_index(op.f('ix_energy_consumptions_id'), 'energy_consumptions', ['id'], unique=False)
    op.drop_column('energy_consumptions', 'consumption_date')
    op.drop_column('energy_consumptions', 'energy_used')
    op.add_column('savings_reports', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('savings_reports', sa.Column('energy_saved', sa.Float(), nullable=False))
    op.add_column('savings_reports', sa.Column('savings', sa.Float(), nullable=False))
    op.add_column('savings_reports', sa.Column('method', sa.String(), nullable=False))
    op.add_column('savings_reports', sa.Column('percentage_saved', sa.Float(), nullable=False))
    op.add_column('savings_reports', sa.Column('units_saved', sa.Float(), nullable=False))
    op.add_column('savings_reports', sa.Column('remarks', sa.Text(), nullable=True))
    op.create_index(op.f('ix_savings_reports_id'), 'savings_reports', ['id'], unique=False)
    op.drop_column('savings_reports', 'report_date')
    op.drop_column('savings_reports', 'savings_amount')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('savings_reports', sa.Column('savings_amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.add_column('savings_reports', sa.Column('report_date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_savings_reports_id'), table_name='savings_reports')
    op.drop_column('savings_reports', 'remarks')
    op.drop_column('savings_reports', 'units_saved')
    op.drop_column('savings_reports', 'percentage_saved')
    op.drop_column('savings_reports', 'method')
    op.drop_column('savings_reports', 'savings')
    op.drop_column('savings_reports', 'energy_saved')
    op.drop_column('savings_reports', 'date')
    op.add_column('energy_consumptions', sa.Column('energy_used', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False))
    op.add_column('energy_consumptions', sa.Column('consumption_date', sa.DATE(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_energy_consumptions_id'), table_name='energy_consumptions')
    op.drop_column('energy_consumptions', 'remarks')
    op.drop_column('energy_consumptions', 'location')
    op.drop_column('energy_consumptions', 'source')
    op.drop_column('energy_consumptions', 'cost')
    op.drop_column('energy_consumptions', 'consumption')
    op.drop_column('energy_consumptions', 'time')
    op.drop_column('energy_consumptions', 'date')
    # ### end Alembic commands ###