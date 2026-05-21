"""Optional helper for creating Elastic indices in production mode.

This is intentionally lightweight for hackathon portability. For the demo, the
backend can run without a live Elastic instance. For a real Elastic Cloud setup,
extend this script with authenticated Elasticsearch client calls.
"""

INDICES = [
    "crowd_telemetry",
    "transport_status",
    "weather_events",
    "social_sentiment",
    "vendor_inventory",
    "incident_history",
    "action_audit_log",
]

if __name__ == "__main__":
    for index in INDICES:
        print(f"create index if missing: {index}")
