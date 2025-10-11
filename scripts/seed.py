import os
from uuid import UUID
from decimal import Decimal
from sqlalchemy import select

from app.db import SessionContext
from app.models import Loan

DUMMY_LOANS = [
    {"id": "00000000-0000-0000-0000-000000000001", "borrower_id": "usr_kenya_001", "amount": Decimal("12500.00"), "currency": "KES", "status": "pending", "term_months": 6, "interest_rate_apr": Decimal("28.00")},
    {"id": "00000000-0000-0000-0000-000000000002", "borrower_id": "usr_india_002", "amount": Decimal("50000.00"), "currency": "INR", "status": "approved", "term_months": 12, "interest_rate_apr": Decimal("24.00")},
    {"id": "00000000-0000-0000-0000-000000000003", "borrower_id": "usr_nigeria_003", "amount": Decimal("32000.00"), "currency": "NGN", "status": "rejected", "term_months": 9, "interest_rate_apr": Decimal("30.00")},
    {"id": "00000000-0000-0000-0000-000000000004", "borrower_id": "usr_vietnam_004", "amount": Decimal("8400.00"), "currency": "VND", "status": "disbursed", "term_months": 4, "interest_rate_apr": Decimal("26.00")},
    {"id": "00000000-0000-0000-0000-000000000005", "borrower_id": "usr_philippines_005", "amount": Decimal("21000.00"), "currency": "PHP", "status": "repaid", "term_months": 6, "interest_rate_apr": Decimal("22.00")},
]

def upsert_dummy_data():
    with SessionContext() as session:
        inserted = 0
        for row in DUMMY_LOANS:
            loan_id = UUID(row["id"]) if "id" in row else None
            existing = session.get(Loan, loan_id) if loan_id else None
            if existing:
                continue
            loan = Loan(
                id=loan_id,
                borrower_id=row["borrower_id"],
                amount=row["amount"],
                currency=row["currency"],
                status=row["status"],
                term_months=row.get("term_months"),
                interest_rate_apr=row.get("interest_rate_apr"),
            )
            session.add(loan)
            inserted += 1
        print(f"Seed complete. Inserted {inserted} rows.")

if __name__ == "__main__":
    upsert_dummy_data()
