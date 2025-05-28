FROM public.ecr.aws/docker/library/python:3.11.12 AS build

WORKDIR /app

RUN pip install uv

COPY uv.lock pyproject.toml /app/

RUN uv sync

FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

COPY --from=build /app/.venv /app/.venv

COPY . .

EXPOSE 8000

CMD ["/app/.venv/bin/uvicorn", "--app-dir", "app", "sample.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
