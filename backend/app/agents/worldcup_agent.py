from __future__ import annotations
from app.models.schemas import Telemetry, AgentPlan
from app.services.elastic_mcp import ElasticMCPClient

class WorldCupOpsAgent:
    def __init__(self, mcp: ElasticMCPClient) -> None:
        self.mcp = mcp

    async def analyze(self, telemetry: Telemetry) -> AgentPlan:
        calls = []
        crowd = await self.mcp.get_current_crowd_telemetry(telemetry.zone)
        calls.append(f"{crowd['tool']} -> {crowd['index']} for {telemetry.zone}")
        transport = await self.mcp.get_related_transport_logs()
        calls.append(f"{transport['tool']} -> {transport['index']} for stadium delay logs")
        weather = await self.mcp.get_weather_events()
        calls.append(f"{weather['tool']} -> {weather['index']} for rain impact")
        similar = await self.mcp.vector_search_similar_incidents(telemetry)
        calls.append(f"{similar['tool']} -> {similar['index']} top similarity {similar['top_match']['similarity']}")

        return AgentPlan(
            incident="Gate B rain-amplified crowd congestion",
            severity="high",
            root_causes=[
                "Crowd density exceeded safe operating threshold at Gate B.",
                "Heavy rain slowed manual ticket and security processing.",
                "Stadium Express bus delays caused compressed late arrivals.",
                "Negative fan sentiment indicates rising frustration and safety risk.",
            ],
            recommended_actions=[
                "Open Gate D as an overflow entry lane.",
                "Reroute incoming fans from Gate B to Gates C and D.",
                "Dispatch 8 stewards to Zone B for queue splitting.",
                "Send a multilingual fan advisory with updated gate guidance.",
                "Create an Elastic audit entry and monitor recovery every 60 seconds.",
            ],
            estimated_impact="Expected to reduce Gate B density by 35% and wait time by 11 minutes within 12-15 minutes.",
            risk_analysis=[
                "Opening overflow access requires operator approval.",
                "Public advisory must be accurate to avoid sending fans into another bottleneck.",
                "Rollback is available by closing overflow routing and restoring default gate instructions.",
            ],
            requires_approval=True,
            elastic_mcp_calls=calls,
        )
