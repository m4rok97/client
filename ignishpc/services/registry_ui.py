import os

import docker
import docker.types

from ignishpc.common import network
from ignishpc.common import configuration


def _container_name():
    return "ignishpc-registry-ui"


def _start(args):
    client = docker.from_env()
    name = _container_name()
    image = configuration.format_image("registry-ui")

    port = args.port
    if port is None:
        port = 3000

    url = args.url
    if url is None:
        url = "http://" + network.get_local_ip() + ":5000"
    if url.endswith("/"):
        url = url[:-1]

    environment = {
        "SINGLE_REGISTRY": "true",
        "NGINX_PROXY_PASS_URL": url,
        "DELETE_IMAGES": "true",
        "REGISTRY_TITLE": "IgnisHPC",
        "NGINX_LISTEN_PORT": str(port)
    }

    for var in args.env:
        key, value = var.split("=", 1)
        environment[key] = value

    client.containers.run(
        image=image,
        name=name,
        detach=True,
        environment=environment,
        mounts=[docker.types.Mount(source=path, target=path, type="bind") for path in args.volume],
        ports={port: port},
        restart_policy={"Name": "always"}
    )
