## Overview

This project is a simple monitoring API built with FastAPI as part of the Day 2 lab.

The objective is to refactor an existing CLI monitoring script into an object-oriented Python application and expose it through a REST API implementing CRUD operations.

The API allows you to:

* Register new servers
* List monitored servers
* Retrieve a specific server
* Delete a server
* Trigger health checks on demand
* Filter servers by health status

---

## Project Structure

```text
day2-lab/
├── __init__.py
├── main.py
├── models.py
├── health.py
├── config.py
├── servers.json
├── requirements.txt
└── README.md
```

### Files Description

| File               | Description                            |
| ------------------ | -------------------------------------- |
| `main.py`          | FastAPI application and CRUD endpoints |
| `models.py`        | Dataclasses and Pydantic schemas       |
| `health.py`        | Asynchronous health checking logic     |
| `config.py`        | Configuration loader for JSON files    |
| `servers.json`     | Initial list of monitored servers      |
| `requirements.txt` | Python dependencies                    |

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn[standard] httpx
```

Or install directly from requirements:

```bash
pip install -r requirements.txt
```

---

## Running the API

Start the FastAPI server:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

ReDoc documentation:

```text
http://localhost:8000/redoc
```

---

## Server Configuration

The application supports loading monitored servers from a JSON configuration file.

Example `servers.json`:

```json
[
  {
    "name": "api-prod-1",
    "host": "httpbin.org",
    "port": 443,
    "protocol": "https",
    "health_path": "/status/200"
  },
  {
    "name": "api-prod-2",
    "host": "httpbin.org",
    "port": 443,
    "protocol": "https",
    "health_path": "/status/503"
  },
  {
    "name": "slow-server",
    "host": "httpbin.org",
    "port": 443,
    "protocol": "https",
    "health_path": "/delay/6"
  },
  {
    "name": "unreachable",
    "host": "10.255.255.1",
    "port": 8080,
    "protocol": "http",
    "health_path": "/health"
  }
]
```

---

## Health Status Rules

The monitoring system assigns one of the following statuses:

| Status     | Description                                                            |
| ---------- | ---------------------------------------------------------------------- |
| `UP`       | Server responds with HTTP 200 and response time is below the threshold |
| `DEGRADED` | Server responds slowly or returns a non-200 status code                |
| `DOWN`     | Server is unreachable or times out                                     |

Default timeout:

```text
5 seconds
```

Default degraded threshold:

```text
500 ms
```

---

## API Endpoints

### API Health

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "servers_monitored": 4
}
```

---

### Register a Server

```http
POST /servers
```

Example request:

```json
{
  "name": "my-api",
  "host": "example.com",
  "port": 443,
  "protocol": "https",
  "health_path": "/health",
  "tags": ["production", "frontend"]
}
```

---

### List All Servers

```http
GET /servers
```

---

### Filter by Status

```http
GET /servers?status=UP
```

Possible values:

* `UP`
* `DEGRADED`
* `DOWN`
* `unknown`

---

### Get a Server

```http
GET /servers/{server_id}
```

Example:

```http
GET /servers/1
```

---

### Delete a Server

```http
DELETE /servers/{server_id}
```

Example:

```http
DELETE /servers/2
```

---

### Trigger a Health Check

```http
POST /servers/{server_id}/check
```

Example:

```http
POST /servers/1/check
```

---

## Example Workflow

### Register a server

```bash
curl -X POST http://localhost:8000/servers \
-H "Content-Type: application/json" \
-d '{
  "name": "api-prod-1",
  "host": "httpbin.org",
  "port": 443,
  "protocol": "https",
  "health_path": "/status/200"
}'
```

### Trigger a check

```bash
curl -X POST http://localhost:8000/servers/1/check
```

### List healthy servers

```bash
curl http://localhost:8000/servers?status=UP
```

---

## Technologies Used

* Python 3.12+
* FastAPI
* Uvicorn
* HTTPX
* Pydantic
* AsyncIO

---

## Future Improvements

Possible enhancements include:

* API Key authentication
* Persistent storage with SQLite or PostgreSQL
* Prometheus metrics export
* Health check history
* Background scheduled checks
* Docker support
* Kubernetes deployment
* Retry and backoff strategies

---

## Author

Developed as part of a DevOps training lab focused on:

* Object-Oriented Programming
* Asynchronous Python
* REST APIs
* Monitoring concepts
* FastAPI development
