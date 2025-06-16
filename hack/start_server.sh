#!/usr/bin/env bash

/app/.venv/bin/python manage.py collectstatic --noinput

exec /app/.venv/bin/uvicorn --app-dir app sample.asgi:application --host 0.0.0.0 --port 8000
