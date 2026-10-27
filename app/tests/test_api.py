import pytest
from src import create_app
from src.models import db, Incident, Vehicle, EmergencyUnit

@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        # Seed test vehicle and unit
        v = Vehicle(
            vin="TESTVIN1234567890",
            license_plate="TE26 ABC",
            make="TestMake",
            model="TestModel",
            owner_name="Test Driver",
            emergency_contact_name="Test Contact",
            emergency_contact_phone="+44 7700 900000",
            iot_device_id="IOT-TEST-01"
        )
        u = EmergencyUnit(
            unit_code="TEST-AMB-01",
            service_type="Ambulance (NHS)",
            station_name="Test Station",
            base_city="London",
            current_lat=51.5,
            current_lng=-0.1,
            status="Available"
        )
        db.session.add(v)
        db.session.add(u)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"
    assert data["version"] == "2.4.0"

def test_get_stats(client):
    res = client.get("/api/v1/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert "total_incidents" in data
    assert "available_units" in data

def test_ingest_collision_telemetry(client):
    payload = {
        "vehicle_id": 1,
        "location_name": "M25 Junction 14 Test",
        "postcode": "TW6 2AA",
        "latitude": 51.4700,
        "longitude": -0.4543,
        "g_force": 9.5,
        "speed_mph": 55.0,
        "collision_angle": "Frontal",
        "airbag_deployed": True,
        "rollover_detected": False,
        "auto_dispatch": True
    }
    res = client.post("/api/v1/incidents", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["incident"]["severity"] in ["High", "Critical"]
    assert data["auto_dispatched"] is True

def test_architecture_page(client):
    res = client.get("/architecture")
    assert res.status_code == 200
    assert b"Building a Secure &amp; Automated Cloud Infrastructure" in res.data or b"Architecture" in res.data
