# Tier 2: UK Emergency Dispatch Service
import math
from datetime import datetime
from ..models import db, Incident, EmergencyUnit, EmergencyDispatch, AuditLog

class DispatchService:
    """Handles automated and manual dispatch of UK Emergency Services (Ambulance, Police, Fire)."""

    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculates great-circle distance between two GPS coordinates in kilometers."""
        R = 6371.0 # Earth's radius in km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @classmethod
    def find_nearest_units(cls, latitude: float, longitude: float, max_units: int = 3) -> list[tuple[EmergencyUnit, float]]:
        """Finds closest available emergency units within operational range."""
        available_units = EmergencyUnit.query.filter(EmergencyUnit.status.in_(["Available", "Standby"])).all()
        ranked = []
        for unit in available_units:
            dist = cls.haversine_distance_km(latitude, longitude, unit.current_lat, unit.current_lng)
            ranked.append((unit, round(dist, 2)))
        
        ranked.sort(key=lambda x: x[1])
        return ranked[:max_units]

    @classmethod
    def dispatch_units_for_incident(cls, incident_id: int, custom_notes: str = None) -> list[EmergencyDispatch]:
        """Automatically assigns nearest emergency units based on incident severity."""
        incident = db.session.get(Incident, incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found.")

        # Determine how many units are required
        needed_count = 1
        if incident.severity == "Critical":
            needed_count = 3 # Ambulance + Police + Fire & Rescue
        elif incident.severity == "High":
            needed_count = 2 # Ambulance + Police

        nearest = cls.find_nearest_units(incident.latitude, incident.longitude, max_units=needed_count)
        dispatches = []

        for unit, distance_km in nearest:
            # Estimate arrival time (assumes 50 km/h emergency average in UK urban/highway conditions)
            eta_minutes = max(3, int((distance_km / 50.0) * 60) + 2)
            
            dispatch = EmergencyDispatch(
                incident_id=incident.id,
                unit_id=unit.id,
                dispatched_at=datetime.utcnow(),
                estimated_arrival_minutes=eta_minutes,
                status="En Route",
                notes=custom_notes or f"Auto-dispatched via UK Emergency 999 CAD integration. Distance: {distance_km}km"
            )
            unit.status = "En Route"
            db.session.add(dispatch)
            dispatches.append(dispatch)

        incident.status = "Dispatched"
        incident.dispatched_at = datetime.utcnow()

        audit = AuditLog(
            event_type="EMERGENCY_DISPATCHED",
            actor="DISPATCH_ROUTING_SERVICE",
            resource_id=incident.reference_id,
            details=f"Dispatched {len(dispatches)} emergency units to {incident.location_name} (ETA: {dispatches[0].estimated_arrival_minutes if dispatches else 0}m).",
            severity="INFO"
        )
        db.session.add(audit)
        db.session.commit()

        return dispatches
