from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

Severity = Literal["normal", "low", "medium", "high", "critical"]
IncidentStatus = Literal["monitoring", "detected", "awaiting_approval", "executing", "resolving", "resolved", "rolled_back"]

class Telemetry(BaseModel):
    timestamp: datetime
    zone: str
    crowd_density: float = Field(ge=0, le=1)
    wait_time_minutes: int
    throughput_per_minute: int
    transport_delay_minutes: int
    sentiment_score: float = Field(ge=-1, le=1)
    weather: str
    vendor_stock_percent: int = Field(ge=0, le=100)
    severity: Severity

class AgentPlan(BaseModel):
    incident: str
    severity: Severity
    root_causes: list[str]
    recommended_actions: list[str]
    estimated_impact: str
    risk_analysis: list[str]
    requires_approval: bool = True
    elastic_mcp_calls: list[str]

class Incident(BaseModel):
    id: str
    title: str
    zone: str
    status: IncidentStatus
    severity: Severity
    detected_at: datetime
    plan: AgentPlan | None = None
    approved_actions: list[str] = []
    audit_log: list[str] = []

class OpsState(BaseModel):
    telemetry: Telemetry
    active_incident: Incident | None = None
    timeline: list[str]
