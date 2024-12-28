#!/bin/bash
set -e

# Run database migrations
alembic stamp head
alembic revision --autogenerate -m "initial migration"
alembic upgrade head

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port 8001