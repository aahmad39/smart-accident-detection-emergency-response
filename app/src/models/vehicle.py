# Tier 3: Vehicle Telemetry Model
from datetime import datetime
from .incident import db

class Vehicle(db.Model):
    """Connected vehicle registry capturing onboard telemetry and crash diagnostics."""
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vin = db.Column(db.String(50), unique=True, nullable=False, index=True)
    license_plate = db.Column(db.String(15), nullable=False, index=True) # UK format e.g. "LD24 ZKL"
    make = db.Column(db.String(50), nullable=False) # e.g. "Tesla", "BMW", "Nissan"
    model = db.Column(db.String(50), nullable=False) # e.g. "Model Y", "i4", "Leaf"
    year = db.Column(db.Integer, default=2024)
    color = db.Column(db.String(30), default="Black")
    
    # Registered Owner & Emergency Contact (UK GDPR compliant pseudonymized)
    owner_name = db.Column(db.String(100), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=False)
    emergency_contact_phone = db.Column(db.String(20), nullable=False)
    
    # Telematics Status
    iot_device_id = db.Column(db.String(50), unique=True, nullable=False)
    firmware_version = db.Column(db.String(20), default="v4.2.1")
    last_known_speed = db.Column(db.Float, default=0.0)
    battery_level_pct = db.Column(db.Integer, default=85)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    incidents = db.relationship("Incident", back_populates="vehicle")

    def to_dict(self):
        return {
            "id": self.id,
            "vin": self.vin,
            "license_plate": self.license_plate,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "color": self.color,
            "owner_name": self.owner_name,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_phone": self.emergency_contact_phone,
            "iot_device_id": self.iot_device_id,
            "firmware_version": self.firmware_version
        }
