import pytest
from src.services.detection_engine import AccidentDetectionEngine

def test_calculate_crash_severity_critical():
    # Extreme impact rollover
    severity, casualties = AccidentDetectionEngine.calculate_crash_severity(
        g_force=13.5,
        impact_speed_mph=70.0,
        airbag=True,
        rollover=True
    )
    assert severity == "Critical"
    assert casualties >= 1

def test_calculate_crash_severity_high():
    # High G impact without rollover
    severity, casualties = AccidentDetectionEngine.calculate_crash_severity(
        g_force=8.2,
        impact_speed_mph=45.0,
        airbag=True,
        rollover=False
    )
    assert severity == "High"

def test_calculate_crash_severity_minor():
    # Low speed parking contact
    severity, casualties = AccidentDetectionEngine.calculate_crash_severity(
        g_force=2.1,
        impact_speed_mph=15.0,
        airbag=False,
        rollover=False
    )
    assert severity == "Minor"
    assert casualties == 0
