from flask import Blueprint, jsonify
from sqlalchemy import text
from app.db import SessionContext

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health():
    try:
        with SessionContext() as session:
            session.execute(text("SELECT 1"))

        return jsonify({"status": "healthy", "db": "connected"}), 200

    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
