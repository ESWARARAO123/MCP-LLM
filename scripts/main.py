import json
import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.llm import generate_response
from mcp_client.mcp_client import MCPClient

# Add the root directory to sys.path


# Load configurations
with open("../config/postgres_config.json") as f:
    postgres_config = json.load(f)

with open("../config/grafana_config.json") as f:
    grafana_config = json.load(f)

# Initialize MCP client
mcp_client = MCPClient(postgres_config, grafana_config)

# Fetch data from PostgreSQL
query = """
SELECT 
    beginpoint, endpoint, period, libsetup, checktype, required, arrival, slack
FROM ariane_place_sorted
ORDER BY slack ASC
LIMIT 2;
"""
data = mcp_client.fetch_data_from_postgres(query)

if data:
    print("Data fetched from PostgreSQL:", data)

    # Prepare data for Grafana
    formatted_data = [
        {
            "signal_path": f"{row[0]} -> {row[1]}",
            "period": row[2],
            "libsetup": row[3],
            "checktype": row[4],
            "required_time": row[5],
            "arrival_time": row[6],
            "slack": row[7]
        }
        for row in data
    ]

    # Send data to Grafana
    mcp_client.send_data_to_grafana(formatted_data)

    # Use LLM to generate insights
    prompt = """
    Analyze the ariane_place_sorted and provide actionable insights.
    Key metrics include:
    - Signal Path: The path between beginpoint and endpoint.
    - Period: The clock period.
    - Slack: The difference between required and arrival times.
    - Required Time: The time by which the signal must arrive.
    - Arrival Time: The actual time when the signal arrives.

    Identify potential bottlenecks or areas for optimization.
    Focus on paths with negative slack values, as they indicate timing violations.
    """
    insights = generate_response(prompt)
    print("LLM Insights:", insights)
else:
    print("No data fetched from PostgreSQL.")

# Logging
logging.basicConfig(
    filename="../logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Application started.")