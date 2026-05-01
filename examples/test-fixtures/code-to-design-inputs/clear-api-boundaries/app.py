"""Patient vitals monitoring API — Flask application."""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration
DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.getenv("API_KEY", "dev-key")
MAX_RESULTS_PER_PAGE = 100
RATE_LIMIT_RPM = 60


@app.route("/api/v1/patients", methods=["GET"])
def list_patients():
    """List all active patients with pagination."""
    page = request.args.get("page", 1, type=int)
    return jsonify({"patients": [], "page": page})


@app.route("/api/v1/patients/<patient_id>/vitals", methods=["GET"])
def get_patient_vitals(patient_id: str):
    """Retrieve vitals for a specific patient."""
    return jsonify({"patient_id": patient_id, "vitals": []})


@app.route("/api/v1/alerts", methods=["POST"])
def create_alert():
    """Create a new clinical alert."""
    data = request.get_json()
    return jsonify({"alert_id": "ALT-001", "status": "created"}), 201


@app.route("/api/v1/export", methods=["POST"])
def export_data():
    """Export patient data in FHIR format."""
    return jsonify({"export_id": "EXP-001"})
