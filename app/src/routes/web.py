# Tier 1: Web Presentation Controller
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Incident, Vehicle, EmergencyUnit, EmergencyDispatch, AuditLog
from ..services import AccidentDetectionEngine, DispatchService

web_bp = Blueprint("web", __name__)

@web_bp.route("/")
def dashboard():
    """Main live operations and emergency control room dashboard."""
    total_incidents = Incident.query.count()
    active_critical = Incident.query.filter(Incident.severity.in_(["Critical", "High"]), Incident.status != "Resolved").count()
    dispatched_units = EmergencyUnit.query.filter_by(status="En Route").count()
    total_vehicles = Vehicle.query.count()

    recent_incidents = Incident.query.order_by(Incident.timestamp.desc()).limit(6).all()
    recent_dispatches = EmergencyDispatch.query.order_by(EmergencyDispatch.dispatched_at.desc()).limit(5).all()
    recent_audits = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(5).all()

    return render_template(
        "index.html",
        total_incidents=total_incidents,
        active_critical=active_critical,
        dispatched_units=dispatched_units,
        total_vehicles=total_vehicles,
        recent_incidents=recent_incidents,
        recent_dispatches=recent_dispatches,
        recent_audits=recent_audits
    )

@web_bp.route("/incidents")
def incidents():
    """Incident registry with severity and status filters."""
    severity_filter = request.args.get("severity")
    status_filter = request.args.get("status")

    query = Incident.query
    if severity_filter:
        query = query.filter_by(severity=severity_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)

    incidents_list = query.order_by(Incident.timestamp.desc()).all()
    return render_template("incidents.html", incidents=incidents_list, selected_severity=severity_filter, selected_status=status_filter)

@web_bp.route("/incidents/<int:incident_id>")
def incident_detail(incident_id):
    """Detailed forensic crash telemetry and dispatch timeline."""
    incident = db.get_or_404(Incident, incident_id)
    return render_template("incident_detail.html", incident=incident)

@web_bp.route("/incidents/<int:incident_id>/dispatch-action", methods=["POST"])
def manual_dispatch(incident_id):
    """Manual dispatch trigger from UI."""
    notes = request.form.get("notes", "Manually authorized by UK Emergency Operator")
    try:
        DispatchService.dispatch_units_for_incident(incident_id, custom_notes=notes)
        flash(f"Emergency units dispatched to Incident #{incident_id} successfully.", "success")
    except Exception as e:
        flash(f"Dispatch error: {str(e)}", "danger")
    return redirect(url_for("web.incident_detail", incident_id=incident_id))

@web_bp.route("/dispatch")
def dispatch_center():
    """UK Emergency Response Teams & active dispatches management."""
    units = EmergencyUnit.query.order_by(EmergencyUnit.service_type, EmergencyUnit.unit_code).all()
    active_dispatches = EmergencyDispatch.query.filter(EmergencyDispatch.status.in_(["Assigned", "En Route", "Arrived"])).all()
    return render_template("dispatch.html", units=units, dispatches=active_dispatches)

@web_bp.route("/simulator")
def simulator():
    """Crash simulation tool for testing end-to-end telemetry and auto-dispatch."""
    vehicles = Vehicle.query.all()
    return render_template("simulator.html", vehicles=vehicles)

@web_bp.route("/architecture")
def architecture():
    """Interactive Cloud Architecture & DevSecOps Topology presentation."""
    return render_template("architecture.html")

@web_bp.route("/ai-hub")
def ai_hub():
    """Azure OpenAI AI Agents control room (Risk, Security, PR Review, Post-Deploy, RCA)."""
    return render_template("ai_hub.html")
