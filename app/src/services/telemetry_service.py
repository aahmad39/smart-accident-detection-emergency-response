# Tier 2: Azure Application Insights & Telemetry Service
import logging
from flask import current_app

logger = logging.getLogger("smart_accident_system")

class TelemetryService:
    """Manages telemetry, metrics, and distributed tracing via Azure Application Insights."""

    _telemetry_client = None

    @classmethod
    def init_telemetry(cls, app):
        """Initializes Azure Monitor OpenTelemetry or opencensus SDK if configured."""
        conn_str = app.config.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
        if conn_str:
            try:
                # Support Azure Monitor OpenTelemetry
                from azure.monitor.opentelemetry import configure_azure_monitor
                configure_azure_monitor(connection_string=conn_str)
                logger.info("Azure Application Insights telemetry initialized successfully.")
            except ImportError:
                logger.warning("azure-monitor-opentelemetry not installed. Telemetry will fallback to local logging.")
            except Exception as e:
                logger.error(f"Failed to initialize Application Insights: {e}")

    @classmethod
    def track_incident_metric(cls, severity: str, g_force: float):
        """Logs custom business metrics for dashboard monitoring."""
        logger.info(f"[METRIC] CollisionDetected - Severity: {severity}, G-Force: {g_force}G")

    @classmethod
    def track_dispatch_event(cls, reference_id: str, units_count: int, eta_minutes: int):
        """Logs emergency dispatch response telemetry."""
        logger.info(f"[METRIC] EmergencyDispatch - Ref: {reference_id}, Units: {units_count}, ETA: {eta_minutes}m")
