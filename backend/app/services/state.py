from __future__ import annotations
from datetime import datetime, timezone
from app.models.schemas import Telemetry, OpsState, Incident

class OpsMemory:
    def __init__(self) -> None:
        self.telemetry = Telemetry(
            timestamp=datetime.now(timezone.utc),
            zone="Gate B",
            crowd_density=0.38,
            wait_time_minutes=4,
            throughput_per_minute=640,
            transport_delay_minutes=3,
            sentiment_score=0.42,
            weather="clear",
            vendor_stock_percent=84,
            severity="normal",
        )
        self.active_incident: Incident | None = None
        self.timeline: list[str] = ["Normal World Cup stadium operations initialized."]
        self.ws_clients = set()

    def snapshot(self) -> OpsState:
        return OpsState(telemetry=self.telemetry, active_incident=self.active_incident, timeline=self.timeline[-20:])

ops_memory = OpsMemory()
