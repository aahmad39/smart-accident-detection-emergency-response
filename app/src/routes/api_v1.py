# Tier 2: RESTful API Layer (v1)
from datetime import datetime
from flask import Blueprint, jsonify, request
from ..models import db, Incident, Vehicle, EmergencyUnit, EmergencyDispatch, AuditLog
from ..services import AccidentDetectionEngine, DispatchService, TelemetryService

api_v1_bp = Blueprint("api_v1", __name__)

@api_v1_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check probe for Azure App Service, Application Insights, and Front Door.
    Returns status of API, Database connectivity, and version.
    """
    db_status = "healthy"
    try:
        # Simple DB check
        Incident.query.limit(1).all()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    status_code = 200 if "healthy" in db_status else 503
    return jsonify({
        "status": "online" if status_code == 200 else "degraded",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "database": db_status,
        "service": "Smart Accident Detection & Emergency Response System (UK)",
        "version": "2.4.0"
    }), status_code

@api_v1_bp.route("/stats", methods=["GET"])
def get_stats():
    """Returns real-time KPI metrics for dashboard."""
    total_incidents = Incident.query.count()
    critical_count = Incident.query.filter_by(severity="Critical").count()
    high_count = Incident.query.filter_by(severity="High").count()
    active_dispatches = EmergencyDispatch.query.filter(EmergencyDispatch.status.in_(["Assigned", "En Route"])).count()
    available_units = EmergencyUnit.query.filter_by(status="Available").count()

    return jsonify({
        "total_incidents": total_incidents,
        "critical_count": critical_count,
        "high_count": high_count,
        "active_dispatches": active_dispatches,
        "available_units": available_units,
        "timestamp": datetime.utcnow().isoformat()
    })

@api_v1_bp.route("/incidents", methods=["GET"])
def get_incidents():
    """List recorded collisions with optional filtering."""
    severity = request.args.get("severity")
    status = request.args.get("status")

    query = Incident.query
    if severity:
        query = query.filter_by(severity=severity)
    if status:
        query = query.filter_by(status=status)

    incidents = query.order_by(Incident.timestamp.desc()).limit(100).all()
    return jsonify([inc.to_dict() for inc in incidents])

@api_v1_bp.route("/incidents", methods=["POST"])
def report_crash_telemetry():
    """
    Ingests live collision telematics from vehicle onboard IoT unit or camera AI.
    Automatically evaluates severity, persists incident, and can trigger emergency dispatch.
    """
    data = request.get_json() or {}
    if not data:
        return jsonify({"error": "Missing JSON payload"}), 400

    try:
        incident = AccidentDetectionEngine.process_telemetry_crash_event(data)
        TelemetryService.track_incident_metric(incident.severity, incident.g_force)

        # Auto-dispatch for Critical/High severity
        auto_dispatched = False
        if incident.severity in ["Critical", "High"] and data.get("auto_dispatch", True):
            DispatchService.dispatch_units_for_incident(incident.id, "Auto-dispatched on severe impact trigger")
            auto_dispatched = True

        return jsonify({
            "message": "Crash incident successfully registered",
            "incident": incident.to_dict(),
            "auto_dispatched": auto_dispatched
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_v1_bp.route("/incidents/<int:incident_id>/dispatch", methods=["POST"])
def dispatch_for_incident(incident_id):
    """Triggers emergency dispatch mission for a specific incident."""
    data = request.get_json() or {}
    notes = data.get("notes")

    try:
        dispatches = DispatchService.dispatch_units_for_incident(incident_id, notes)
        return jsonify({
            "message": f"Successfully dispatched {len(dispatches)} emergency units",
            "dispatches": [d.to_dict() for d in dispatches]
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_v1_bp.route("/units", methods=["GET"])
def get_units():
    """Lists UK emergency units and live availability."""
    units = EmergencyUnit.query.all()
    return jsonify([u.to_dict() for u in units])

@api_v1_bp.route("/simulate", methods=["POST"])
def simulate_crash():
    """Generates a realistic simulated UK vehicle collision for live demonstrations."""
    data = request.get_json() or {}
    
    # Defaults for a dramatic highway collision (e.g. M25 or M1)
    mock_payload = {
        "location_name": data.get("location_name", "M25 Junction 15 (M4 Interchange) London"),
        "postcode": data.get("postcode", "SL3 8QH"),
        "latitude": data.get("latitude", 51.4883),
        "longitude": data.get("longitude", -0.5097),
        "g_force": data.get("g_force", 10.4),
        "speed_mph": data.get("speed_mph", 64.5),
        "airbag_deployed": data.get("airbag_deployed", True),
        "rollover_detected": data.get("rollover_detected", False),
        "collision_angle": data.get("collision_angle", "Side-Impact T-Bone"),
        "vehicle_id": data.get("vehicle_id", 1),
        "auto_dispatch": True
    }

    incident = AccidentDetectionEngine.process_telemetry_crash_event(mock_payload)
    dispatches = DispatchService.dispatch_units_for_incident(incident.id, "Auto-dispatched via simulated emergency 999 link")

    return jsonify({
        "message": "Crash simulation executed successfully",
        "incident": incident.to_dict(),
        "dispatches": [d.to_dict() for d in dispatches]
    }), 201
