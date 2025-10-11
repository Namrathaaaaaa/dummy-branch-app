from datetime import datetime
import uuid
from sqlalchemy import CheckConstraint, Column, String, Numeric, Integer, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from .db import Base

class Loan(Base):
    __tablename__ = "loans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    borrower_id = Column(String, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    status = Column(String, nullable=False)
    term_months = Column(Integer, nullable=True)
    interest_rate_apr = Column(Numeric(5, 2), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    __table_args__ = (
        CheckConstraint("amount > 0 AND amount <= 50000", name="chk_amount_range"),
        CheckConstraint(
            "status IN ('pending','approved','rejected','disbursed','repaid','defaulted')",
            name="chk_status_enum",
        ),
    )
