import docker
import docker.errors
from ignishpc.services import registry
from ignishpc.services import registry_ui


def _actions(m, **kargs):
    return {
        "start": lambda args: _start(args, m),
        "stop": lambda args: _stop(args, m._container_name()),
        "resume": lambda args: _resume(args, m._container_name()),
        "destroy": lambda args: _destroy(args, m._container_name()),
        "status": lambda args: _status(args, m._container_name()),
        **kargs
    }


def _run(args):
    service = {
        "status": _status,
        "registry": _actions(registry, garbage=registry._garbage),
        "registry-ui": _actions(registry_ui)
    }[args.service]
    if "action" in args:
        return service[args.action](args)
    else:
        return service(args)


def _start(args, m):
    client = docker.from_env()
    try:
        c = client.containers.get(m._container_name())
        if args.force:
            c.remove(force=True)
        else:
            raise RuntimeError("Service already exists")
    except docker.errors.NotFound:
        pass
    m._start(args)


def _stop(args, name):
    client = docker.from_env()
    try:
        client.containers.get(name).stop()
    except docker.errors.NotFound:
        raise RuntimeError("Service not found")


def _resume(args, name):
    client = docker.from_env()
    try:
        client.containers.get(name).start()
    except docker.errors.NotFound:
        raise RuntimeError("Service not found")


def _destroy(args, name):
    client = docker.from_env()
    try:
        client.containers.get(name).remove(force=True)
    except docker.errors.NotFound:
        pass


def _status(args, name=None):
    if name is None:
        print("Service Status:")
        print(" ", "Registry".ljust(14), end="  ")
        _status(args, registry._container_name())
        print(" ", "Registry-ui".ljust(14), end="  ")
        _status(args, registry._container_name())
        """
        print(" ", "Nomad  ".ljust(14), end="")
        _status(args, registry._container_name())
        print(" ", "Zookeeper  ".ljust(14), end="")
        _status(args, registry._container_name())
        print(" ", "Mesos  ".ljust(14), end="")
        _status(args, registry._container_name())
        print(" ", "Submitter  ".ljust(14), end="")
        _status(args, registry._container_name())"""
    else:
        client = docker.from_env()
        try:
            print(client.containers.get(name).status.upper())
        except docker.errors.NotFound:
            print("NOT_FOUND")
