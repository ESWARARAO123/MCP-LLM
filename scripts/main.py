import json
from models.llm import generate_response
from mcp_client.mcp_client import MCPClient
import logging

# Load configurations
with open("../config/postgres_config.json") as f:
    postgres_config = json.load(f)

with open("../config/grafana_config.json") as f:
    grafana_config = json.load(f)

# Initialize MCP client
mcp_client = MCPClient(postgres_config, grafana_config)

# Fetch data from PostgreSQL
query = "SELECT product_name, SUM(quantity * price) AS total_sales FROM sales GROUP BY product_name;"
data = mcp_client.fetch_data_from_postgres(query)

if data:
    print("Data fetched from PostgreSQL:", data)

    # Prepare data for Grafana
    formatted_data = [{"product": row[0], "total_sales": row[1]} for row in data]

    # Send data to Grafana
    mcp_client.send_data_to_grafana(formatted_data)

    # Use LLM to generate insights
    prompt = "Analyze the sales data and provide insights."
    insights = generate_response(prompt)
    print("LLM Insights:", insights)
else:
    print("No data fetched from PostgreSQL.")
logging.basicConfig(
    filename="../logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Application started.")