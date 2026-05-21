from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from app.models.schemas import Telemetry, Incident
from app.services.state import ops_memory

async def broadcast() -> None:
    data = ops_memory.snapshot().model_dump_json()
    dead = []
    for ws in ops_memory.ws_clients:
        try:
            await ws.send_text(data)
        except Exception:
            dead.append(ws)
    for ws in dead:
        ops_memory.ws_clients.discard(ws)

async def normal_tick() -> None:
    t = ops_memory.telemetry
    if ops_memory.active_incident and ops_memory.active_incident.status in {"executing", "resolving"}:
        density = max(0.48, t.crowd_density - 0.08)
        wait = max(6, t.wait_time_minutes - 3)
        delay = max(5, t.transport_delay_minutes - 2)
        sentiment = min(0.25, t.sentiment_score + 0.18)
        status_sev = "medium" if density > 0.62 else "low"
        if density <= 0.52:
            ops_memory.active_incident.status = "resolved"
            ops_memory.active_incident.severity = "low"
            ops_memory.timeline.append("Incident resolved: Gate B operations returned to safe range.")
    else:
        density = min(0.45, max(0.32, t.crowd_density + 0.01))
        wait = max(3, min(6, t.wait_time_minutes))
        delay = max(2, min(5, t.transport_delay_minutes))
        sentiment = min(0.50, max(0.30, t.sentiment_score))
        status_sev = "normal"

    ops_memory.telemetry = Telemetry(
        timestamp=datetime.now(timezone.utc),
        zone="Gate B",
        crowd_density=density,
        wait_time_minutes=wait,
        throughput_per_minute=640 if density < 0.6 else 310,
        transport_delay_minutes=delay,
        sentiment_score=sentiment,
        weather="rain" if ops_memory.active_incident else "clear",
        vendor_stock_percent=ops_memory.telemetry.vendor_stock_percent,
        severity=status_sev,
    )
    await broadcast()

async def run_simulator() -> None:
    while True:
        await normal_tick()
        await asyncio.sleep(2)

def inject_gate_b_surge() -> Incident:
    now = datetime.now(timezone.utc)
    ops_memory.telemetry = Telemetry(
        timestamp=now,
        zone="Gate B",
        crowd_density=0.92,
        wait_time_minutes=18,
        throughput_per_minute=210,
        transport_delay_minutes=24,
        sentiment_score=-0.71,
        weather="heavy_rain",
        vendor_stock_percent=61,
        severity="high",
    )
    incident = Incident(
        id="INC-GATEB-2026-001",
        title="Gate B crowd surge during rain and transport delay",
        zone="Gate B",
        status="detected",
        severity="high",
        detected_at=now,
        audit_log=["Anomaly detected from live telemetry stream."],
    )
    ops_memory.active_incident = incident
    ops_memory.timeline.append("Injected demo incident: Gate B congestion, rain, transport delays, negative sentiment.")
    return incident
