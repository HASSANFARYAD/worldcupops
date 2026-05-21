from __future__ import annotations
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.services.state import ops_memory
from app.simulator.engine import inject_gate_b_surge, broadcast, run_simulator
from app.agents.worldcup_agent import WorldCupOpsAgent
from app.services.elastic_mcp import ElasticMCPClient

app = FastAPI(title="WorldCupOps Agent API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
agent = WorldCupOpsAgent(ElasticMCPClient())

@app.on_event("startup")
async def startup() -> None:
    asyncio.create_task(run_simulator())

@app.get("/health")
async def health():
    return {"status": "ok", "service": "worldcupops-agent"}

@app.get("/api/state")
async def state():
    return ops_memory.snapshot()

@app.post("/api/simulator/inject/gate-b-surge")
async def inject():
    incident = inject_gate_b_surge()
    await broadcast()
    return incident

@app.post("/api/agent/analyze")
async def analyze():
    if not ops_memory.active_incident:
        inject_gate_b_surge()
    plan = await agent.analyze(ops_memory.telemetry)
    ops_memory.active_incident.plan = plan
    ops_memory.active_incident.status = "awaiting_approval"
    ops_memory.active_incident.audit_log.append("Gemini agent generated mitigation plan using Elastic MCP context.")
    ops_memory.timeline.append("Agent completed investigation and requested operator approval.")
    await broadcast()
    return ops_memory.active_incident

@app.post("/api/incidents/{incident_id}/approve")
async def approve(incident_id: str):
    incident = ops_memory.active_incident
    if not incident or incident.id != incident_id:
        return {"error": "incident not found"}
    actions = incident.plan.recommended_actions if incident.plan else []
    incident.approved_actions = actions
    incident.status = "executing"
    incident.audit_log.append("Operator approved critical mitigation actions.")
    for action in actions:
        incident.audit_log.append(f"Executed: {action}")
    ops_memory.timeline.append("Approved actions executed: overflow gate, rerouting, stewards, fan advisory, audit log.")
    await broadcast()
    return incident

@app.post("/api/incidents/{incident_id}/rollback")
async def rollback(incident_id: str):
    incident = ops_memory.active_incident
    if not incident or incident.id != incident_id:
        return {"error": "incident not found"}
    incident.status = "rolled_back"
    incident.audit_log.append("Rollback executed: restored default routing and paused public advisories.")
    ops_memory.timeline.append("Rollback executed by operator.")
    await broadcast()
    return incident

@app.websocket("/ws/ops")
async def ws_ops(ws: WebSocket):
    await ws.accept()
    ops_memory.ws_clients.add(ws)
    try:
        await ws.send_text(ops_memory.snapshot().model_dump_json())
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        ops_memory.ws_clients.discard(ws)
