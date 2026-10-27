# Tier 3: Security & Operational Audit Log Model
from datetime import datetime
from .incident import db

class AuditLog(db.Model):
    """DevSecOps compliance and audit trail recording critical actions, dispatches, and alerts."""
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False, index=True) # e.g. "CRASH_DETECTED", "999_DISPATCH", "SECURITY_ALERT"
    actor = db.Column(db.String(100), default="SYSTEM_AI_ENGINE")
    resource_id = db.Column(db.String(100), nullable=True)
    details = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45), default="127.0.0.1")
    severity = db.Column(db.String(20), default="INFO") # INFO, WARN, ERROR, CRITICAL

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "event_type": self.event_type,
            "actor": self.actor,
            "resource_id": self.resource_id,
            "details": self.details,
            "severity": self.severity
        }
