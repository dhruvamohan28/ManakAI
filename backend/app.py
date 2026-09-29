from flask import Flask, request, jsonify
from flask_cors import CORS

from ai_standards_team1a.analyzer import analyze_procurement_specification

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "message": "Team 1B backend is running"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request must contain valid JSON"
        }), 400

    specification = data.get("specification", "")

    if not specification:
        return jsonify({
            "error": "specification is required"
        }), 400

    if not isinstance(specification, str):
        return jsonify({
            "error": "specification must be a string"
        }), 400

    try:
        result = analyze_procurement_specification(specification)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": "Analysis failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )