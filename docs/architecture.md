# Architecture

WorldCupOps is a demo-ready event operations platform composed of five layers.

## 1. Frontend dashboard

Next.js dashboard for operators:

- live KPIs,
- operations map,
- incident status,
- AI reasoning panel,
- Elastic MCP call trace,
- human approval buttons,
- audit timeline.

## 2. Backend API

FastAPI service exposing:

- REST APIs for incident flow,
- WebSocket stream for live updates,
- simulator controller,
- agent orchestration,
- approval and rollback actions.

## 3. Simulator

Generates demo telemetry for:

- crowd density,
- wait time,
- gate throughput,
- transport delay,
- weather,
- fan sentiment.

## 4. Gemini agent

The agent performs:

- anomaly interpretation,
- multi-factor root cause analysis,
- MCP tool selection,
- mitigation planning,
- structured action recommendation.

## 5. Elastic MCP layer

Elastic provides:

- telemetry search,
- vector incident retrieval,
- operational logs,
- action audit trails,
- observability dashboard foundation.
