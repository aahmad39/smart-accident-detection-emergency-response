// Smart Accident Response - Main Frontend Interactivity
document.addEventListener('DOMContentLoaded', () => {
    console.log("Smart Accident Response System initialized.");

    // Auto-refresh stats every 15 seconds if on dashboard
    if (document.getElementById('kpi-total-incidents')) {
        setInterval(refreshDashboardStats, 15000);
    }
});

async function refreshDashboardStats() {
    try {
        const res = await fetch('/api/v1/stats');
        if (!res.ok) return;
        const data = await res.json();
        
        const totalEl = document.getElementById('kpi-total-incidents');
        const critEl = document.getElementById('kpi-critical-incidents');
        const dispEl = document.getElementById('kpi-dispatched-units');
        
        if (totalEl) totalEl.innerText = data.total_incidents;
        if (critEl) critEl.innerText = data.critical_count + data.high_count;
        if (dispEl) dispEl.innerText = data.active_dispatches;
    } catch (e) {
        console.warn("Telemetry polling transient error:", e);
    }
}
