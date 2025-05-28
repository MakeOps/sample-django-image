import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

app = Celery("tasks", broker=REDIS_URL)

@app.task
def add(x, y):
    return x + y
