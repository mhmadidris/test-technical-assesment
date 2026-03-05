# Customer Data Pipeline Project

This project is a simple data pipeline system consisting of three main services running within Docker:
1. **mock-server** (Flask): Serves customer data from a JSON file.
2. **pipeline-service** (FastAPI): Ingests data from the mock-server into PostgreSQL using the `dlt` library.
3. **postgres**: The database storage for customer data.

---

## Project Structure
```text
.
├── docker-compose.yml
├── mock-server/          # Flask API (Port 5000)
│   ├── app/              # Application logic & routes
│   ├── data/             # JSON data source (customers.json)
│   └── run.py            # Flask entry point
└── pipeline-service/     # FastAPI Service (Port 8000)
    ├── models/           # SQLAlchemy Models
    ├── services/         # Ingestion logic (dlt)
    └── main.py           # FastAPI Routes
```

---

## How to Run (Docker Compose)

### 1. Preparation
Ensure **Docker Desktop** is running and ports **5000, 8000, and 5432** are not being used by other applications (especially the AirPlay Receiver on macOS, which often occupies port 5000).

### 2. Build and Run
Execute the following command in the project's root directory:
```bash
docker-compose up --build
```

---

## Main API Endpoints

### 1. Mock Server (Port 5000)
- `GET /api/customers` : List of customers from JSON (supports `page` & `limit` params).
- `GET /api/customers/{id}` : Details of a single customer.
- `GET /api/health` : Service health check.

### 2. Pipeline Service (Port 8000)
- `POST /api/ingest` : Fetches data from Flask and inserts it into PostgreSQL (Upsert logic).
- `GET /api/customers` : Retrieves the list of customers directly from PostgreSQL.
- `GET /api/customers/{id}` : Customer details from the database.
- `GET /docs` : Interactive Swagger UI documentation.

---

## Database Connection (DBeaver / Others)
- **Host**: `localhost`
- **Port**: `5432`
- **Database**: `customer_db`
- **User**: `postgres`
- **Password**: `password`
- **JDBC URL**: `jdbc:postgresql://localhost:5432/customer_db`

---

## Data Workflow
1. The **mock-server** service loads data from `data/customers.json`.
2. Trigger the pipeline by calling `POST http://localhost:8000/api/ingest`.
3. The **pipeline-service** fetches the data, parses the dates, and saves them into **PostgreSQL**.
4. The data is then ready to be accessed via the FastAPI API on port 8000.
