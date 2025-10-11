"""create loans table

Revision ID: 0001
Revises: 
Create Date: 2025-10-11 00:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'loans',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('borrower_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('term_months', sa.Integer(), nullable=True),
        sa.Column('interest_rate_apr', sa.Numeric(5, 2), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("amount > 0 AND amount <= 50000", name="chk_amount_range"),
        sa.CheckConstraint("status IN ('pending','approved','rejected','disbursed','repaid','defaulted')", name="chk_status_enum"),
    )


def downgrade() -> None:
    op.drop_table('loans')
