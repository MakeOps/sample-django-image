import os
import httpx


ECS_CONTAINER_METADATA_URI_V4 = os.environ.get("ECS_CONTAINER_METADATA_URI_V4")


def get_fargate_ip_address():
    response = httpx.get(f"{ECS_CONTAINER_METADATA_URI_V4}/task")
    return response.json()["Networks"][0]["IPv4Addresses"][0]
