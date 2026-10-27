# Database Seed Script: UK Emergency Units, Vehicles & Real-world Incidents
from datetime import datetime, timedelta
import random
from .models import db, Incident, Vehicle, EmergencyUnit, EmergencyDispatch, AuditLog

def seed_database():
    """Populates realistic UK data if tables are empty."""
    if Vehicle.query.first():
        print("Database already contains data. Skipping seed.")
        return

    print("Seeding initial UK emergency vehicles, units, and incidents...")

    # 1. Registered Connected Vehicles (UK format)
    vehicles = [
        Vehicle(
            vin="SALWA2VF8NA198231",
            license_plate="LD24 ZKL",
            make="Range Rover",
            model="Velar P400e",
            year=2024,
            color="Santorini Black",
            owner_name="Alexander Wright",
            emergency_contact_name="Victoria Wright",
            emergency_contact_phone="+44 7700 900142",
            iot_device_id="IOT-VEH-UK-8801",
            firmware_version="v4.8.2"
        ),
        Vehicle(
            vin="5YJ3E1EB8NF837192",
            license_plate="BJ73 TUV",
            make="Tesla",
            model="Model Y Long Range",
            year=2023,
            color="Pearl White",
            owner_name="Sophia Davies",
            emergency_contact_name="James Davies",
            emergency_contact_phone="+44 7700 900591",
            iot_device_id="IOT-VEH-UK-8802",
            firmware_version="v4.9.1"
        ),
        Vehicle(
            vin="WBA33AY08NFP28471",
            license_plate="MA72 KPM",
            make="BMW",
            model="i4 eDrive40",
            year=2023,
            color="Portimao Blue",
            owner_name="Mohammed Patel",
            emergency_contact_name="Amina Patel",
            emergency_contact_phone="+44 7700 900823",
            iot_device_id="IOT-VEH-UK-8803",
            firmware_version="v4.8.0"
        ),
        Vehicle(
            vin="WAUZZZF27N1084920",
            license_plate="EA24 GHY",
            make="Audi",
            model="Q4 e-tron",
            year=2024,
            color="Daytona Grey",
            owner_name="Oliver Thompson",
            emergency_contact_name="Emma Thompson",
            emergency_contact_phone="+44 7700 900334",
            iot_device_id="IOT-VEH-UK-8804",
            firmware_version="v4.9.0"
        ),
        Vehicle(
            vin="VF1RJB00867192039",
            license_plate="WN22 XRT",
            make="Nissan",
            model="Ariya Evolve",
            year=2022,
            color="Akatsuki Copper",
            owner_name="Charlotte Evans",
            emergency_contact_name="David Evans",
            emergency_contact_phone="+44 7700 900712",
            iot_device_id="IOT-VEH-UK-8805",
            firmware_version="v4.7.5"
        )
    ]
    for v in vehicles:
        db.session.add(v)
    db.session.commit()

    # 2. UK Emergency Units (London Ambulance NHS, Met Police, London Fire Brigade, West Midlands, Greater Manchester)
    units = [
        EmergencyUnit(
            unit_code="LAS-MED-101",
            service_type="Ambulance (NHS)",
            station_name="London Ambulance Service - Waterloo Base",
            base_city="London",
            current_lat=51.5033,
            current_lng=-0.1195,
            status="Available",
            contact_radio="Airwave TETRA 101",
            crew_size=2
        ),
        EmergencyUnit(
            unit_code="LAS-HART-40",
            service_type="Ambulance (NHS Hazardous Area Response)",
            station_name="London Ambulance HART Deptford",
            base_city="London",
            current_lat=51.4783,
            current_lng=-0.0267,
            status="Available",
            contact_radio="Airwave TETRA 140",
            crew_size=4
        ),
        EmergencyUnit(
            unit_code="MET-POL-99",
            service_type="Police (Metropolitan)",
            station_name="Met Police Traffic Garage - Alperton",
            base_city="London",
            current_lat=51.5401,
            current_lng=-0.2988,
            status="Available",
            contact_radio="Met Radio Ch 4",
            crew_size=2
        ),
        EmergencyUnit(
            unit_code="LFB-RES-07",
            service_type="Fire & Rescue (London)",
            station_name="London Fire Brigade - Lambeth",
            base_city="London",
            current_lat=51.4925,
            current_lng=-0.1160,
            status="Available",
            contact_radio="LFB Command 07",
            crew_size=5
        ),
        EmergencyUnit(
            unit_code="WMAS-AMB-22",
            service_type="Ambulance (NHS West Midlands)",
            station_name="Birmingham Central Station",
            base_city="Birmingham",
            current_lat=52.4862,
            current_lng=-1.8904,
            status="Available",
            contact_radio="WMAS Direct 22",
            crew_size=2
        ),
        EmergencyUnit(
            unit_code="NWAS-AMB-88",
            service_type="Ambulance (NHS North West)",
            station_name="Manchester Central Ambulance Base",
            base_city="Manchester",
            current_lat=53.4808,
            current_lng=-2.2426,
            status="Available",
            contact_radio="NWAS Dispatch 88",
            crew_size=2
        )
    ]
    for u in units:
        db.session.add(u)
    db.session.commit()

    # 3. Seed Realistic Historical & Active Incidents across UK
    now = datetime.utcnow()
    incidents = [
        Incident(
            reference_id="CAD-UK-2026-9812",
            timestamp=now - timedelta(minutes=14),
            location_name="M25 Motorway Junction 14 near Heathrow Airport",
            postcode="TW6 2AA",
            latitude=51.4700,
            longitude=-0.4543,
            severity="Critical",
            g_force=11.8,
            impact_speed_mph=68.4,
            airbag_deployed=True,
            rollover_detected=True,
            collision_angle="Multiple-Vehicle Pileup",
            status="Dispatched",
            estimated_casualties=2,
            emergency_services_notified=True,
            dispatched_at=now - timedelta(minutes=12),
            vehicle_id=vehicles[0].id
        ),
        Incident(
            reference_id="CAD-UK-2026-9804",
            timestamp=now - timedelta(minutes=45),
            location_name="A40 Western Avenue, Acton, London",
            postcode="W3 0BP",
            latitude=51.5205,
            longitude=-0.2678,
            severity="High",
            g_force=8.6,
            impact_speed_mph=52.0,
            airbag_deployed=True,
            rollover_detected=False,
            collision_angle="Side T-Bone Collision",
            status="On-Scene",
            estimated_casualties=1,
            emergency_services_notified=True,
            dispatched_at=now - timedelta(minutes=42),
            vehicle_id=vehicles[1].id
        ),
        Incident(
            reference_id="CAD-UK-2026-9791",
            timestamp=now - timedelta(hours=2, minutes=10),
            location_name="M1 Motorway Junction 6A (M25 Interchange), Watford",
            postcode="WD25 0LZ",
            latitude=51.6934,
            longitude=-0.3845,
            severity="Medium",
            g_force=5.4,
            impact_speed_mph=38.2,
            airbag_deployed=True,
            rollover_detected=False,
            collision_angle="Rear-End Shunt",
            status="Resolved",
            estimated_casualties=1,
            emergency_services_notified=True,
            dispatched_at=now - timedelta(hours=2, minutes=8),
            resolved_at=now - timedelta(hours=1, minutes=15),
            vehicle_id=vehicles[2].id
        ),
        Incident(
            reference_id="CAD-UK-2026-9745",
            timestamp=now - timedelta(hours=5),
            location_name="Spaghetti Junction (M6 J6), Birmingham",
            postcode="B6 7AA",
            latitude=52.5113,
            longitude=-1.8624,
            severity="Minor",
            g_force=3.1,
            impact_speed_mph=21.0,
            airbag_deployed=False,
            rollover_detected=False,
            collision_angle="Low-Speed Barrier Scrape",
            status="Resolved",
            estimated_casualties=0,
            emergency_services_notified=False,
            dispatched_at=None,
            resolved_at=now - timedelta(hours=4, minutes=40),
            vehicle_id=vehicles[3].id
        )
    ]
    for inc in incidents:
        db.session.add(inc)
    db.session.commit()

    # 4. Link Dispatches for the active incident
    active_inc = incidents[0]
    amb_unit = units[0]
    pol_unit = units[2]
    amb_unit.status = "En Route"
    pol_unit.status = "En Route"

    d1 = EmergencyDispatch(
        incident_id=active_inc.id,
        unit_id=amb_unit.id,
        dispatched_at=now - timedelta(minutes=12),
        estimated_arrival_minutes=6,
        status="En Route",
        notes="High-priority NHS trauma response unit assigned to M25 Junction 14 rollover."
    )
    d2 = EmergencyDispatch(
        incident_id=active_inc.id,
        unit_id=pol_unit.id,
        dispatched_at=now - timedelta(minutes=12),
        estimated_arrival_minutes=4,
        status="En Route",
        notes="Met Police Traffic patrol en route for motorway lane closure and scene management."
    )
    db.session.add(d1)
    db.session.add(d2)

    # 5. Initial Audit Logs
    audits = [
        AuditLog(
            event_type="SYSTEM_BOOT",
            actor="AZURE_APP_SERVICE",
            resource_id="uksouth-appservice-linux",
            details="3-Tier Monolithic Smart Accident Response System initialized on Azure.",
            severity="INFO"
        ),
        AuditLog(
            event_type="CRASH_DETECTED",
            actor="IOT-VEH-UK-8801",
            resource_id=active_inc.reference_id,
            details=f"Severe rollover collision detected on M25. 11.8G impact. Dispatched 999 priority CAD alert.",
            severity="CRITICAL"
        )
    ]
    for a in audits:
        db.session.add(a)

    db.session.commit()
    print("Database seeding completed successfully.")
