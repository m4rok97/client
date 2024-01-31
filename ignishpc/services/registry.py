import os

import docker
import docker.errors
import docker.types

from ignishpc.common import network
from ignishpc.common import configuration


def _container_name():
    return "ignishpc-registry"


def _start(args):
    client = docker.from_env()
    name = _container_name()
    environment = dict.fromkeys([entry.split("=", 1) for entry in args.env])

    https = args.https or "REGISTRY_HTTP_TLS_CERTIFICATE" in environment
    image = configuration.format_image("registry")

    path = args.path
    if path is None:
        path = "/var/lib/ignis/registry"

    port = args.port
    if port is None:
        port = 443 if https else 5000

    if "REGISTRY_HTTP_ADDR" not in environment:
        environment["REGISTRY_HTTP_ADDR"] = ("0.0.0.0" if args.bind is None else args.bind) + ":" + str(port)

    if "REGISTRY_STORAGE_DELETE_ENABLED" not in environment:
        environment["REGISTRY_STORAGE_DELETE_ENABLED"] = "true"

    mounts = [docker.types.Mount(source=path, target="/var/lib/registry", type="bind")]
    if args.https:
        environment["REGISTRY_HTTP_TLS_CERTIFICATE"] = "/etc/ignis/registry/domain.crt"
        environment["REGISTRY_HTTP_TLS_KEY"] = "/etc/ignis/registry/domain.key"
        environment["REGISTRY_HTTP_SECRET"] = "/etc/ignis/registry/secret"
        mounts.append(docker.types.Mount(source="/etc/ignis/registry", target="/etc/ignis/registry", type="bind"))

        if os.path.exists(environment["REGISTRY_HTTP_TLS_CERTIFICATE"]) and \
                os.path.exists(environment["REGISTRY_HTTP_TLS_KEY"]):
            print("certificates found")
        else:
            print("certificates not found, generating self-sign certificate")
            cmd = ("req -newkey rsa:2048 -nodes -sha256 "
                   f"-keyout {environment['REGISTRY_HTTP_TLS_KEY']} -x509 -days 365 "
                   f"-out {environment['REGISTRY_HTTP_TLS_CERTIFICATE']} "
                   "-subj '/C=ig/ST=ignis/L=ignis/O=ignis/CN=www.ignishpc.readthedocs.io'")
            client.containers.run(image=image,
                                  command=cmd,
                                  remove=True,
                                  entrypoint="openssl",
                                  mounts=mounts)
        if not os.path.exists(environment["REGISTRY_HTTP_SECRET"]):
            print("secret not found, generating random")
            with open(environment["REGISTRY_HTTP_SECRET"], "w") as file:
                file.write(configuration.random_password(16))
                file.flush()

    client.containers.run(
        image=image,
        name=name,
        detach=True,
        environment=environment,
        mounts=mounts,
        ports={port: port} if args.bind is None else {port: (port, network.get_local_ip())},
        restart_policy={"Name": "always"}
    )

    bind = args.bind or network.get_address()

    if not https:
        print(f'info: add \'{{"insecure-registries" : [ "{bind}:{port}" ]}}\' '
              'to /etc/docker/daemon.json and restart docker daemon service')
    else:
        print(f"info: execute 'cp /etc/ignis/registry/domain.crt /etc/docker/certs.d/{bind}:{port}/ca.crt' when use "
              "self-sign certificate")

    print(f"      use {bind}:{port} to refer the registry")


def _garbage(args):
    client = docker.from_env()
    try:
        container = client.containers.get(_container_name())
        if container.status.upper() != "RUNNING":
            raise RuntimeError("registry is not RUNNING")
        cmd = ["bin/registry", "garbage-collect", "/etc/docker/registry/config.yml"]
        if args.delete_untagged:
            cmd.insert(2, "-m")
        print(container.exec_run(cmd).output.decode("utf-8"))
    except docker.errors.NotFound:
        raise RuntimeError("registry is not found")
