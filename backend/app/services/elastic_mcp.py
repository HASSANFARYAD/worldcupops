from __future__ import annotations
from app.models.schemas import Telemetry

class ElasticMCPClient:
    """Demo-compatible facade for Elastic MCP.

    In production, replace these methods with calls to the Elastic MCP server.
    Keeping this explicit makes the demo judge-friendly: the UI can display each
    MCP-style tool call and its purpose.
    """

    async def get_current_crowd_telemetry(self, zone: str) -> dict:
        return {"tool": "elastic.search", "index": "crowd_telemetry", "zone": zone}

    async def get_related_transport_logs(self) -> dict:
        return {"tool": "elastic.search", "index": "transport_status", "query": "delays near stadium"}

    async def get_weather_events(self) -> dict:
        return {"tool": "elastic.search", "index": "weather_events", "query": "rain impact gate throughput"}

    async def vector_search_similar_incidents(self, telemetry: Telemetry) -> dict:
        return {
            "tool": "elastic.vector_search",
            "index": "incident_history",
            "top_match": {
                "incident_type": "rain-amplified gate congestion",
                "successful_actions": ["open overflow gate", "reroute arrivals", "send advisory", "dispatch stewards"],
                "resolution_time_minutes": 14,
                "similarity": 0.91,
            },
        }

    async def index_incident_summary(self, incident_id: str, summary: dict) -> dict:
        return {"tool": "elastic.index", "index": "incident_history", "incident_id": incident_id, "status": "indexed"}

    async def write_action_audit(self, incident_id: str, action: str) -> dict:
        return {"tool": "elastic.index", "index": "action_audit_log", "incident_id": incident_id, "action": action}
