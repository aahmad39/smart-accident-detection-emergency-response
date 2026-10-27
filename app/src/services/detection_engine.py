# Tier 2: Accident Detection & Impact Analysis Engine
import uuid
import math
from datetime import datetime
from ..models import db, Incident, Vehicle, AuditLog

class AccidentDetectionEngine:
    """Core intelligence engine for processing IoT vehicle telematics and detecting severe collisions."""

    @staticmethod
    def calculate_crash_severity(g_force: float, impact_speed_mph: float, airbag: bool, rollover: bool) -> tuple[str, int]:
        """
        Calculates collision severity level and estimated casualties based on sensor inputs.
        UK Road Safety & Emergency Response Standard Classification:
        - Critical: Extreme G-force (>=12G), rollover, high-speed impact (>60mph)
        - High: G-force >= 7.5G, airbag deployed, speed >= 40mph
        - Medium: G-force 4G - 7.5G, moderate speed
        - Minor: Low G-force (<4G), bumper contact, no rollover or airbag
        """
        severity_score = 0
        severity_score += min(g_force * 3.5, 45) # G-force weight
        severity_score += min(impact_speed_mph * 0.4, 30) # Speed weight
        if airbag:
            severity_score += 15
        if rollover:
            severity_score += 25

        if rollover or severity_score >= 70 or g_force >= 12.0:
            severity = "Critical"
            estimated_casualties = 2 if rollover else 1
        elif severity_score >= 45 or g_force >= 7.5 or (airbag and impact_speed_mph >= 35):
            severity = "High"
            estimated_casualties = 1
        elif severity_score >= 25 or g_force >= 4.0:
            severity = "Medium"
            estimated_casualties = 1
        else:
            severity = "Minor"
            estimated_casualties = 0

        return severity, estimated_casualties

    @classmethod
    def process_telemetry_crash_event(cls, telemetry_data: dict) -> Incident:
        """
        Ingests IoT telematics from connected vehicles or crash sensors,
        evaluates crash parameters, persists the incident, and generates audit log.
        """
        g_force = float(telemetry_data.get("g_force", 8.2))
        impact_speed = float(telemetry_data.get("speed_mph", 48.0))
        airbag = bool(telemetry_data.get("airbag_deployed", True))
        rollover = bool(telemetry_data.get("rollover_detected", False))
        angle = telemetry_data.get("collision_angle", "Frontal Impact")

        severity, casualties = cls.calculate_crash_severity(g_force, impact_speed, airbag, rollover)

        # Generate UK NHS/Police style Computer Aided Dispatch (CAD) reference
        ref_id = f"CAD-UK-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}"

        incident = Incident(
            reference_id=ref_id,
            timestamp=datetime.utcnow(),
            location_name=telemetry_data.get("location_name", "M25 Junction 14 near Heathrow"),
            postcode=telemetry_data.get("postcode", "TW6 2AA"),
            latitude=float(telemetry_data.get("latitude", 51.4700)),
            longitude=float(telemetry_data.get("longitude", -0.4543)),
            severity=severity,
            g_force=g_force,
            impact_speed_mph=impact_speed,
            airbag_deployed=airbag,
            rollover_detected=rollover,
            collision_angle=angle,
            status="Detected",
            estimated_casualties=casualties,
            emergency_services_notified=True,
            evidence_image_url=telemetry_data.get("evidence_image_url"),
            vehicle_id=telemetry_data.get("vehicle_id")
        )

        db.session.add(incident)

        # Create Security/Audit trail
        audit = AuditLog(
            event_type="CRASH_DETECTED",
            actor=f"VEHICLE_IOT_{telemetry_data.get('vehicle_id', 'UNKNOWN')}",
            resource_id=ref_id,
            details=f"Collision detected ({severity} severity) at {incident.location_name}. G-Force: {g_force}G, Speed: {impact_speed}mph. 999 automated link primed.",
            severity="CRITICAL" if severity in ["Critical", "High"] else "WARN"
        )
        db.session.add(audit)
        db.session.commit()

        return incident
