// IoT Crash Simulator Interactivity

const PRESETS = {
    m25_rollover: {
        location: "M25 Motorway Junction 14 near Heathrow Airport",
        postcode: "TW6 2AA",
        lat: 51.4700,
        lng: -0.4543,
        g_force: 12.8,
        speed: 72,
        angle: "Multiple-Vehicle Pileup",
        airbag: true,
        rollover: true
    },
    a40_tbone: {
        location: "A40 Western Avenue, Acton, London",
        postcode: "W3 0BP",
        lat: 51.5205,
        lng: -0.2678,
        g_force: 8.4,
        speed: 54,
        angle: "Side-Impact T-Bone",
        airbag: true,
        rollover: false
    },
    m1_shunt: {
        location: "M1 Motorway Junction 6A (M25 Interchange), Watford",
        postcode: "WD25 0LZ",
        lat: 51.6934,
        lng: -0.3845,
        g_force: 5.2,
        speed: 38,
        angle: "Rear-End Collision",
        airbag: true,
        rollover: false
    },
    birmingham_scrape: {
        location: "Spaghetti Junction (M6 J6), Birmingham",
        postcode: "B6 7AA",
        lat: 52.5113,
        lng: -1.8624,
        g_force: 2.8,
        speed: 24,
        angle: "Frontal Head-On",
        airbag: false,
        rollover: false
    }
};

function loadPreset(key) {
    const p = PRESETS[key];
    if (!p) return;

    document.getElementById('location_name').value = p.location;
    document.getElementById('postcode').value = p.postcode;
    document.getElementById('latitude').value = p.lat;
    document.getElementById('longitude').value = p.lng;
    document.getElementById('g_force').value = p.g_force;
    document.getElementById('g_force_val').innerText = p.g_force;
    document.getElementById('speed_mph').value = p.speed;
    document.getElementById('speed_val').innerText = p.speed;
    document.getElementById('collision_angle').value = p.angle;
    document.getElementById('airbag_deployed').checked = p.airbag;
    document.getElementById('rollover_detected').checked = p.rollover;
}

async function handleSimulate(e) {
    e.preventDefault();
    const btn = document.getElementById('btn-submit-sim');
    const resultBox = document.getElementById('sim-result-box');

    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Injecting Telemetry Stream...';
    resultBox.innerHTML = `// [CONNECT] Initiating secure mTLS handshake to Azure App Service Ingestion API...\n// Ingesting tri-axial accelerometer burst...`;

    const payload = {
        vehicle_id: parseInt(document.getElementById('vehicle_id').value),
        location_name: document.getElementById('location_name').value,
        postcode: document.getElementById('postcode').value,
        latitude: parseFloat(document.getElementById('latitude').value),
        longitude: parseFloat(document.getElementById('longitude').value),
        g_force: parseFloat(document.getElementById('g_force').value),
        speed_mph: parseFloat(document.getElementById('speed_mph').value),
        collision_angle: document.getElementById('collision_angle').value,
        airbag_deployed: document.getElementById('airbag_deployed').checked,
        rollover_detected: document.getElementById('rollover_detected').checked,
        auto_dispatch: true
    };

    try {
        const resp = await fetch('/api/v1/incidents', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await resp.json();

        if (resp.ok) {
            const inc = data.incident;
            let logMsg = `// [SUCCESS 201] Crash Telemetry Persisted into Azure SQL Database\n`;
            logMsg += `// CAD Reference ID: ${inc.reference_id}\n`;
            logMsg += `// Classification: ${inc.severity.toUpperCase()} SEVERITY (${inc.g_force}G Impact)\n`;
            logMsg += `// Airbag: ${inc.airbag_deployed ? 'DEPLOYED' : 'INACTIVE'} | Rollover: ${inc.rollover_detected ? 'CONFIRMED' : 'NO'}\n`;
            logMsg += `// GPS Sector: ${inc.location_name} [${inc.latitude}, ${inc.longitude}]\n`;
            logMsg += `// ------------------------------------------------------------\n`;
            logMsg += `// [EMERGENCY DISPATCH] Automated UK 999 CAD Triggered!\n`;
            logMsg += `// Response Units Dispatched: ${data.auto_dispatched ? 'YES (Nearest Ambulance & Police En Route)' : 'PENDING OPERATOR'}\n`;
            logMsg += `// Azure Application Insights Metric: CollisionDetected emitted\n`;
            logMsg += `// Azure Blob Storage: Uploading dashcam snapshot to container 'crash-evidence'\n\n`;
            logMsg += `>> Redirecting to Incident Telemetry View in 3 seconds...`;
            
            resultBox.innerHTML = logMsg;

            setTimeout(() => {
                window.location.href = `/incidents/${inc.id}`;
            }, 3000);
        } else {
            resultBox.innerHTML = `// [ERROR ${resp.status}] ${data.error || 'Failed to inject crash telemetry'}`;
        }
    } catch (err) {
        resultBox.innerHTML = `// [NETWORK FAILURE] ${err.message}`;
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-satellite-dish"></i> Inject Telemetry & Trigger Emergency Response';
    }
}
