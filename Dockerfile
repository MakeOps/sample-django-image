FROM public.ecr.aws/docker/library/python:3.11.12 AS build

WORKDIR /app

RUN pip install uv

COPY uv.lock pyproject.toml /app/

RUN uv sync

FROM public.ecr.aws/docker/library/python:3.11-slim

RUN apt-get update && apt-get install curl -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=build /app/.venv /app/.venv

COPY deploy/nginx/server.conf.template /etc/nginx/templates/server.conf.template

VOLUME ["/etc/nginx/templates"]

COPY . .

EXPOSE 8000

# CMD ["/app/.venv/bin/uvicorn", "--app-dir", "app", "sample.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

CMD ["/app/hack/start_server.sh"]
