# Tier 3: Emergency Responder Unit & Dispatch Models
from datetime import datetime
from .incident import db

class EmergencyUnit(db.Model):
    """UK Emergency Response Units (Ambulance, Police, Fire & Rescue)."""
    __tablename__ = "emergency_units"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unit_code = db.Column(db.String(20), unique=True, nullable=False, index=True) # e.g. "LAS-AMB-104", "MET-POL-42"
    service_type = db.Column(db.String(30), nullable=False) # Ambulance (NHS), Police, Fire & Rescue, Air Ambulance
    station_name = db.Column(db.String(100), nullable=False) # e.g. "St Thomas' Hospital Trust", "Met Police Westminster"
    base_city = db.Column(db.String(50), default="London")
    
    # Live coordinates of unit
    current_lat = db.Column(db.Float, nullable=False)
    current_lng = db.Column(db.Float, nullable=False)
    
    # Status
    status = db.Column(db.String(30), default="Available") # Available, En Route, On Scene, Busy, Out of Service
    contact_radio = db.Column(db.String(30), default="Airwave TETRA 802.1")
    crew_size = db.Column(db.Integer, default=2)

    # Relationships
    dispatches = db.relationship("EmergencyDispatch", back_populates="unit")

    def to_dict(self):
        return {
            "id": self.id,
            "unit_code": self.unit_code,
            "service_type": self.service_type,
            "station_name": self.station_name,
            "base_city": self.base_city,
            "current_lat": self.current_lat,
            "current_lng": self.current_lng,
            "status": self.status,
            "contact_radio": self.contact_radio,
            "crew_size": self.crew_size
        }

class EmergencyDispatch(db.Model):
    """Link table representing dispatch mission between an incident and response units."""
    __tablename__ = "emergency_dispatches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    incident_id = db.Column(db.Integer, db.ForeignKey("incidents.id"), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("emergency_units.id"), nullable=False)
    
    dispatched_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    estimated_arrival_minutes = db.Column(db.Integer, default=8)
    actual_arrival_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default="En Route") # Assigned, En Route, Arrived, Patient Extricated, Cleared
    notes = db.Column(db.Text, nullable=True)

    # Relationships
    incident = db.relationship("Incident", back_populates="dispatches")
    unit = db.relationship("EmergencyUnit", back_populates="dispatches")

    def to_dict(self):
        return {
            "id": self.id,
            "incident_id": self.incident_id,
            "unit_code": self.unit.unit_code if self.unit else None,
            "service_type": self.unit.service_type if self.unit else None,
            "dispatched_at": self.dispatched_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "estimated_arrival_minutes": self.estimated_arrival_minutes,
            "status": self.status,
            "notes": self.notes
        }
