from flask import Blueprint, jsonify, request, abort
from sqlalchemy import select
from uuid import UUID
from decimal import Decimal

from ..db import SessionContext
from ..models import Loan
from ..schemas import CreateLoanRequest, LoanOut

bp = Blueprint("loans", __name__)

@bp.route("/loans", methods=["GET"])
def list_loans():
    with SessionContext() as session:
        result = session.execute(select(Loan).order_by(Loan.created_at.desc()))
        loans = [
            LoanOut.model_validate(obj, from_attributes=True).model_dump()
            for obj in result.scalars().all()
        ]
        return jsonify(loans)

@bp.route("/loans/<id>", methods=["GET"])
def get_loan(id: str):
    try:
        loan_id = UUID(id)
    except Exception:
        abort(400, description="Invalid loan id")

    with SessionContext() as session:
        loan = session.get(Loan, loan_id)
        if not loan:
            abort(404)
        return jsonify(LoanOut.model_validate(loan, from_attributes=True).model_dump())

@bp.route("/loans", methods=["POST"])
def create_loan():
    payload = request.get_json(silent=True) or {}
    try:
        data = CreateLoanRequest(**payload)
    except Exception as e:
        abort(400, description=str(e))

    with SessionContext() as session:
        loan = Loan(
            borrower_id=data.borrower_id,
            amount=Decimal(str(data.amount)),
            currency=data.currency.upper(),
            term_months=data.term_months,
            interest_rate_apr=(Decimal(str(data.interest_rate_apr)) if data.interest_rate_apr is not None else None),
            status="pending",
        )
        session.add(loan)
        session.flush()
        return jsonify(LoanOut.model_validate(loan, from_attributes=True).model_dump()), 201
