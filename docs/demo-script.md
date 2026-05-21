# 3-Minute Demo Script

## 0:00-0:25 — Problem

Large events like the World Cup produce thousands of signals: crowds, weather, transport, vendors, security, and fan sentiment. Operators do not need another chatbot. They need an AI incident commander that can act under human oversight.

## 0:25-0:50 — Normal operations

Show the WorldCupOps dashboard with stable metrics. Point out live telemetry, Gate B status, and no active incidents.

## 0:50-1:15 — Inject incident

Click **Inject Incident**.

Gate B density jumps above 90%, wait time rises, rain begins, buses are delayed, and fan sentiment drops.

## 1:15-1:55 — Agent investigates

Click **Run Agent**.

Explain that Gemini is using Elastic MCP to query current crowd telemetry, transport logs, weather events, and vector-search similar historical incidents.

## 1:55-2:25 — Human approval

Show the generated plan:

- open Gate D overflow lane,
- reroute fans,
- dispatch stewards,
- send multilingual advisory,
- log the action in Elastic.

Click **Approve Actions**.

## 2:25-2:50 — Execute and recover

Show recovery metrics improving: crowd density, wait time, and sentiment move back toward normal.

## 2:50-3:00 — Close

WorldCupOps turns Gemini + Elastic MCP into a real-time operational command agent for mega-events.
