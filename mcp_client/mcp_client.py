import psycopg2
import requests

class MCPClient:
    def __init__(self, postgres_config, grafana_config):
        self.postgres_config = postgres_config
        self.grafana_config = grafana_config

    def fetch_data_from_postgres(self, query):
        """Fetch data from PostgreSQL."""
        try:
            conn = psycopg2.connect(**self.postgres_config)
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Error fetching data from PostgreSQL: {e}")
            return None

    def send_data_to_grafana(self, data):
        """Send data to Grafana for visualization."""
        url = f"{self.grafana_config['url']}/api/datasources/proxy/{self.grafana_config['datasource_id']}"
        headers = {"Authorization": f"Bearer {self.grafana_config['api_key']}"}
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print("Data sent to Grafana successfully.")
            else:
                print(f"Failed to send data to Grafana: {response.text}")
        except Exception as e:
            print(f"Error sending data to Grafana: {e}")