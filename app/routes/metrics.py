from flask import Blueprint, Response
from prometheus_client import Counter, Histogram, generate_latest

metrics_bp = Blueprint("metrics", __name__)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

RESPONSE_TIME = Histogram(
    "http_request_duration_seconds",
    "Response time in seconds",
    ["endpoint"]
)

@metrics_bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")
