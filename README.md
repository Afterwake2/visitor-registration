# Visitor Registration (Flask + PostgreSQL)

A minimal visitor registration app. Collects:
- First Name, Last Name
- Contact Number
- Company Name (optional)
- Purpose of Visit
- Contact Person

## Run Locally (Docker Compose)

```bash
docker compose up --build
# App: http://localhost:8080
# DB:  postgres://postgres:postgres@localhost:5432/visitor_db
