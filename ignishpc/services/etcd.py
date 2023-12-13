import shlex

import docker
import docker.types

from ignishpc.common import network
from ignishpc.common import configuration


def _container_name():
    return "ignishpc-etcd"


def _start(args):
    client = docker.from_env()
    name = _container_name()
    image = configuration.format_image("etcd")

    ports = {}

    port = args.port
    if port is None:
        port = 2379

    if args.bind is None:
        ports[port] = port
    else:
        ports[port] = (port, args.bind)

    for eport in args.extra_port:
        ports[eport] = eport

    path = args.path
    if path is None:
        path = "/var/lib/ignis/etcd"

    mounts = [docker.types.Mount(source=path, target="/var/lib/etcd", type="bind"),
              docker.types.Mount(source="/etc/ignis/etcd", target="/etc/ignis/etcd", type="bind")]

    extra = shlex.split(args.extra_args, posix=False) if args.extra_args is not None else []
    cmd = []
    s = ""
    if args.secure:
        if "--key-file" not in extra:
            cmd.append("--auto-tls")
        s = "s"

    url = f"http{s}://{network.get_address()}:{port}"
    cmd += ["--name", "ignis", "--data-dir", "/var/lib/etcd",
            "--advertise-client-urls", url,
            "--listen-client-urls", f"http{s}://0.0.0.0:{port}"]

    client.containers.run(
        image=image,
        name=name,
        detach=True,
        entrypoint="/usr/local/bin/etcd",
        command=cmd,
        mounts=mounts,
        ports=ports,
        restart_policy={"Name": "always"}
    )

    print(f"client-url: {url}")
