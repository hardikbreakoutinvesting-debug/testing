"""
app.py
Flask REST API for the calculator app.

Endpoints:
  POST /calculate   – perform a calculation
  GET  /operations  – list supported operations
  GET  /health      – health check
"""

from flask import Flask, request, jsonify
from calculator.operations import calculate, CalculatorError, OPERATIONS

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Simple health-check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.route("/operations", methods=["GET"])
def list_operations():
    """Return the list of supported operations."""
    return jsonify({"operations": list(OPERATIONS.keys())}), 200


@app.route("/calculate", methods=["POST"])
def calculate_endpoint():
    """
    Perform a calculation.

    Request body (JSON):
        {
            "operation": "add" | "subtract" | "multiply" | "divide" | "power" | "modulo",
            "a": <number>,
            "b": <number>
        }

    Response (JSON):
        {
            "operation": "add",
            "a": 10,
            "b": 5,
            "result": 15
        }
    """
    data = request.get_json(silent=True)

    # --- Validate request body ---
    if not data:
        return jsonify({"error": "Request body must be valid JSON."}), 400

    missing = [field for field in ("operation", "a", "b") if field not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    operation = data["operation"]
    a = data["a"]
    b = data["b"]

    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        return jsonify({"error": "'a' and 'b' must be numbers."}), 400

    # --- Perform calculation ---
    try:
        result = calculate(operation, a, b)
    except CalculatorError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({
        "operation": operation,
        "a": a,
        "b": b,
        "result": result,
    }), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=9000)
