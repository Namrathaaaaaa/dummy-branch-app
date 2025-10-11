from flask import Blueprint, jsonify
from sqlalchemy import select, func

from ..db import SessionContext
from ..models import Loan

bp = Blueprint("stats", __name__)

@bp.route("/stats", methods=["GET"])
def get_stats():
    with SessionContext() as session:
        total_count = session.execute(select(func.count(Loan.id))).scalar_one()
        total_amount = session.execute(select(func.coalesce(func.sum(Loan.amount), 0))).scalar_one()
        avg_amount = session.execute(select(func.coalesce(func.avg(Loan.amount), 0))).scalar_one()

        by_status_rows = session.execute(select(Loan.status, func.count(Loan.id)).group_by(Loan.status)).all()
        by_currency_rows = session.execute(select(Loan.currency, func.count(Loan.id)).group_by(Loan.currency)).all()

        by_status = {k: v for k, v in by_status_rows}
        by_currency = {k: v for k, v in by_currency_rows}

        return jsonify({
            "total_loans": int(total_count),
            "total_amount": float(total_amount),
            "avg_amount": float(avg_amount),
            "by_status": by_status,
            "by_currency": by_currency,
        })
