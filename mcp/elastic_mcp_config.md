# Elastic MCP Integration

WorldCupOps uses Elastic as the partner-powered operational intelligence layer.

## MCP server

Use Elastic's MCP server for Elasticsearch access from the Gemini agent.

Production configuration should expose tools equivalent to:

```json
{
  "mcpServers": {
    "elastic-worldcupops": {
      "command": "npx",
      "args": ["-y", "@elastic/mcp-server-elasticsearch"],
      "env": {
        "ELASTICSEARCH_URL": "${ELASTICSEARCH_URL}",
        "ELASTICSEARCH_API_KEY": "${ELASTICSEARCH_API_KEY}"
      }
    }
  }
}
```

## Tool calls shown in the demo

The demo surfaces these MCP-style calls visibly in the dashboard:

1. `elastic.search -> crowd_telemetry`
2. `elastic.search -> transport_status`
3. `elastic.search -> weather_events`
4. `elastic.vector_search -> incident_history`
5. `elastic.index -> incident_history`
6. `elastic.index -> action_audit_log`

## Why Elastic is meaningful

Elastic is not decorative in this project. It is the operational memory system that lets the agent search live telemetry, retrieve similar incidents, store actions, and support observability.

## Indices

- `crowd_telemetry`
- `transport_status`
- `weather_events`
- `social_sentiment`
- `vendor_inventory`
- `incident_history`
- `action_audit_log`

## Judge-facing explanation

WorldCupOps demonstrates partner power by letting Gemini reason with real operational signals through Elastic MCP. The agent uses Elastic to ground decisions in live data and historical incident memory before asking a human operator to approve critical actions.
