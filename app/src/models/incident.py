# Tier 3: Database Models
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Incident(db.Model):
    """Accident incident record tracking detected vehicular collisions and emergency response status."""
    __tablename__ = "incidents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reference_id = db.Column(db.String(36), unique=True, nullable=False, index=True) # UK NHS/Police CAD format e.g. CAD-UK-2026-9812
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Location details (UK-centric)
    location_name = db.Column(db.String(255), nullable=False) # e.g. "M25 Junction 14 near Heathrow Airport"
    postcode = db.Column(db.String(12), nullable=True) # e.g. "TW6 2AA"
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Collision Telemetrics
    severity = db.Column(db.String(20), default="Medium", nullable=False) # Minor, Medium, High, Critical
    g_force = db.Column(db.Float, nullable=False) # e.g. 9.4 G
    impact_speed_mph = db.Column(db.Float, nullable=False) # e.g. 58.2 mph
    airbag_deployed = db.Column(db.Boolean, default=False, nullable=False)
    rollover_detected = db.Column(db.Boolean, default=False, nullable=False)
    collision_angle = db.Column(db.String(50), default="Frontal") # Frontal, Rear-End, Side T-Bone, Multiple-Vehicle
    
    # Emergency Response Status
    status = db.Column(db.String(30), default="Detected", nullable=False) # Detected, Dispatched, On-Scene, Resolved, Closed
    estimated_casualties = db.Column(db.Integer, default=1)
    emergency_services_notified = db.Column(db.Boolean, default=True) # 999 automated link
    dispatched_at = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    
    # Cloud Storage / Media evidence
    evidence_image_url = db.Column(db.String(512), nullable=True) # Azure Blob Storage URL
    telemetry_blob_path = db.Column(db.String(512), nullable=True)
    
    # Relationships
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=True)
    vehicle = db.relationship("Vehicle", back_populates="incidents")
    dispatches = db.relationship("EmergencyDispatch", back_populates="incident", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "reference_id": self.reference_id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "location_name": self.location_name,
            "postcode": self.postcode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "severity": self.severity,
            "g_force": self.g_force,
            "impact_speed_mph": self.impact_speed_mph,
            "airbag_deployed": self.airbag_deployed,
            "rollover_detected": self.rollover_detected,
            "collision_angle": self.collision_angle,
            "status": self.status,
            "estimated_casualties": self.estimated_casualties,
            "emergency_services_notified": self.emergency_services_notified,
            "dispatched_at": self.dispatched_at.strftime("%Y-%m-%d %H:%M:%S UTC") if self.dispatched_at else None,
            "resolved_at": self.resolved_at.strftime("%Y-%m-%d %H:%M:%S UTC") if self.resolved_at else None,
            "evidence_image_url": self.evidence_image_url,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None
        }
