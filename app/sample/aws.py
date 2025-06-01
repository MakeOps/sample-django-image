import os
import requests

ECS_CONTAINER_METADATA_URI_V4 = os.environ.get("ECS_CONTAINER_METADATA_URI_V4")


def get_fargate_ip_address():
    response = requests.get(f"{ECS_CONTAINER_METADATA_URI_V4}/task")
    response_json = response.json()

    web_container = [container for container in response_json["Containers"] if container["Name"] == "web"][0]
    return web_container["Networks"][0]["IPv4Addresses"][0]


if __name__ == "__main__":
    print(get_fargate_ip_address())
