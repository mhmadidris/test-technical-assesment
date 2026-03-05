import requests
import dlt
import os
from datetime import datetime, date
from sqlalchemy import text
from database import engine

MOCK_SERVER_URL = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000/api/customers")

def fetch_all_from_mock():
    all_data = []
    page = 1
    limit = 10
    
    while True:
        response = requests.get(f"{MOCK_SERVER_URL}/?page={page}&limit={limit}")
        if response.status_code != 200:
            break
            
        res_json = response.json()
        data = res_json.get("data", [])
        if not data:
            break
            
        # Parse date strings to python objects
        for item in data:
            if item.get("date_of_birth"):
                item["date_of_birth"] = date.fromisoformat(item["date_of_birth"])
            if item.get("created_at"):
                # Handle 'Z' suffix for ISO format in Python < 3.11
                dt_str = item["created_at"].replace('Z', '+00:00')
                item["created_at"] = datetime.fromisoformat(dt_str)
            
        all_data.extend(data)
        if len(all_data) >= res_json.get("total", 0):
            break
        page += 1
    
    return all_data

async def run_ingestion():
    data = fetch_all_from_mock()
    
    if not data:
        return 0

    # Configure dlt for postgres
    pipeline = dlt.pipeline(
        pipeline_name="customer_ingestion",
        destination="postgres",
        dataset_name="public"
    )
    
    # Sync URL for dlt
    sync_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@postgres:5432/customer_db").replace("+asyncpg", "")
    os.environ["DESTINATION__POSTGRES__CREDENTIALS"] = sync_url

    # Run the pipeline with merge write_disposition for upsert
    info = pipeline.run(
        data,
        table_name="customers",
        write_disposition="merge",
        primary_key="customer_id"
    )
    
    return len(data)
